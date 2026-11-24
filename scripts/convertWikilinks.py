#!/usr/bin/env python3
"""Convert Obsidian wikilinks to standard Markdown links for Zensical

Supported wikilink forms (``!`` embeds are NOT converted, only reported)::

    [[Page]]                  -> [Page](Page.md)
    [[Page|alias]]            -> [alias](Page.md)
    [[Page#Heading]]          -> [Page > Heading](Page.md#heading)
    [[Page#Heading|alias]]    -> [alias](Page.md#heading)
    [[#Heading]]              -> [Heading](#heading)
    [[#Heading|alias]]        -> [alias](#heading)
    [[Folder/Page]]           -> path is resolved relative to the linking file

Inside Markdown tables Obsidian requires the alias separator to be escaped
(``[[Page\\|alias]]``); both ``|`` and ``\\|`` are accepted

Wikilinks inside fenced code blocks, inline code spans and YAML front matter
are left untouched

Usage::

    python3 scripts/convert_wikilinks.py                # convert files in place
    python3 scripts/convert_wikilinks.py --dry-run      # only report, write nothing
    python3 scripts/convert_wikilinks.py --strict       # exit 1 on unresolved links

The script rewrites files in place, so run it on a copy (or in CI), not on
your Obsidian vault
"""
from __future__ import annotations

import argparse
import os
import re
import sys
import urllib.parse
from pathlib import Path

# Directories that are never scanned (in addition to every dot-directory)
DEFAULT_SKIP_DIRS = {"site", "scripts", "node_modules", "venv"}
# Files that are never scanned or used as link targets
SKIP_SUFFIXES = (".excalidraw.md",)

WIKILINK_RE = re.compile(r"(?<!!)\[\[([^\[\]\n]+?)\]\]")
EMBED_RE = re.compile(r"!\[\[([^\[\]\n]+?)\]\]")
ALIAS_SPLIT_RE = re.compile(r"\\?\|")
INLINE_CODE_RE = re.compile(r"(?<!`)(`+)(?!`)(.+?)(?<!`)\1(?!`)")
FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
HEADING_RE = re.compile(r"^ {0,3}(#{1,6})[ \t]+(.+?)[ \t]*#*[ \t]*$")


def slugify(heading: str) -> str:
    """Return the HTML id Markdown generates for a heading.

    Lowercase, drop punctuation, collapse whitespace/hyphens to a single '-'.
    Assumption: Zensical uses this same scheme. Verify against the built site
    (see the note in the chat), because I could not run a build here
    """
    s = re.sub(r"[^\w\s-]", "", heading.strip().lower())
    return re.sub(r"[-\s]+", "-", s).strip("-")


def clean_heading_text(text: str) -> str:
    """Strip inline Markdown from a heading so it matches the generated id."""
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)  # links / images
    text = re.sub(r"[`*_~]", "", text)  # code marks, emphasis
    return text


def iter_markdown_files(root: Path, skip_dirs: set[str]):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(
            d for d in dirnames if not d.startswith(".") and d not in skip_dirs
        )
        for name in sorted(filenames):
            if name.endswith(".md") and not name.endswith(SKIP_SUFFIXES):
                yield Path(dirpath) / name


def split_front_matter(lines: list[str]) -> int:
    """Return the index of the first line after YAML front matter (or 0)"""
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() in ("---", "..."):
                return i + 1
    return 0


def collect_headings(text: str) -> dict[str, int]:
    """Map slug -> number of headings with that slug (outside code fences)"""
    lines = text.splitlines()
    slugs: dict[str, int] = {}
    fence: tuple[str, int] | None = None
    for line in lines[split_front_matter(lines):]:
        m = FENCE_RE.match(line)
        if m:
            marker = m.group(1)
            if fence is None:
                fence = (marker[0], len(marker))
            elif marker[0] == fence[0] and len(marker) >= fence[1]:
                fence = None
            continue
        if fence is not None:
            continue
        h = HEADING_RE.match(line)
        if h:
            slug = slugify(clean_heading_text(h.group(2)))
            slugs[slug] = slugs.get(slug, 0) + 1
    return slugs


class Converter:
    def __init__(self, root: Path, skip_dirs: set[str], dry_run: bool):
        self.root = root.resolve()
        self.dry_run = dry_run
        self.problems = 0
        self.converted = 0
        self.files = [p.resolve() for p in iter_markdown_files(self.root, skip_dirs)]
        self.by_path: dict[str, Path] = {}  # "folder/page" (no ext, lowercase)
        self.by_name: dict[str, list[Path]] = {}  # "page.md" / "file.ext"
        self.by_stem: dict[str, list[Path]] = {}  # "page"
        # Non-Markdown files (LICENSE.txt, images, ...) can be link targets too,
        # but are only matched by their full file name
        for dirpath, dirnames, filenames in os.walk(self.root):
            dirnames[:] = [
                d for d in dirnames if not d.startswith(".") and d not in skip_dirs
            ]
            for name in filenames:
                if not name.startswith(".") and not name.endswith(".md"):
                    self.by_name.setdefault(name.lower(), []).append(Path(dirpath) / name)
        for p in self.files:
            rel = p.relative_to(self.root).as_posix()
            self.by_path[rel[:-3].lower()] = p
            self.by_name.setdefault(p.name.lower(), []).append(p)
            self.by_stem.setdefault(p.stem.lower(), []).append(p)
        self._headings: dict[Path, dict[str, int]] = {}

    # -- diagnostics --------------------------------------------------------
    def warn(self, path: Path, lineno: int, message: str) -> None:
        self.problems += 1
        rel = path.relative_to(self.root).as_posix()
        if os.environ.get("GITHUB_ACTIONS") == "true":
            print(f"::warning file={rel},line={lineno}::{message}")
        else:
            print(f"warning: {rel}:{lineno}: {message}")

    # -- resolution ---------------------------------------------------------
    def resolve_page(self, page: str, source: Path) -> tuple[Path | None, str | None]:
        """Return (target file, error message)"""
        key = page.strip().replace("\\", "/")
        if key.lower().endswith(".md"):
            key = key[:-3]
        if key.lower() in self.by_path:
            return self.by_path[key.lower()], None
        name = Path(page).name.lower()
        for candidates in (
            self.by_name.get(name),
            self.by_stem.get(Path(key).name.lower()),
        ):
            if candidates:
                if len(candidates) > 1:
                    chosen = sorted(candidates, key=lambda p: len(p.parts))[0]
                    return chosen, (
                        f"ambiguous page '{page}', using "
                        f"{chosen.relative_to(self.root).as_posix()}"
                    )
                return candidates[0], None
        return None, f"page '{page}' not found"

    def headings_of(self, path: Path) -> dict[str, int]:
        if path not in self._headings:
            self._headings[path] = collect_headings(path.read_text(encoding="utf-8"))
        return self._headings[path]

    # -- conversion --
    def convert_link(self, inner: str, source: Path, lineno: int) -> str:
        target, alias = (
            ALIAS_SPLIT_RE.split(inner, maxsplit=1) if ALIAS_SPLIT_RE.search(inner)
            else (inner, None)
        )
        page, header = target.split("#", 1) if "#" in target else (target, None)
        page = page.strip()
        header = header.strip() if header is not None else None
        if header and header.startswith("^"):
            self.warn(source, lineno, f"block reference '[[{inner}]]' is not supported")
            header = None
        if header and "#" in header:  # [[Page#H1#H2]] -> last heading
            header = header.rsplit("#", 1)[1].strip()

        if alias is not None and alias.strip():
            label = alias.strip()
        elif not page:
            label = header or ""
        else:
            label = f"{page} > {header}" if header else page
        label = label.replace("[", "\\[").replace("]", "\\]")

        anchor = f"#{slugify(header)}" if header else ""

        if not page:  # same-page heading link
            if header:
                self.check_heading(source, source, header, lineno)
            return f"[{label}]({anchor})"

        target_file, error = self.resolve_page(page, source)
        if error:
            self.warn(source, lineno, error)
        if target_file is None:
            href = urllib.parse.quote(f"{page}.md", safe="/")
        else:
            rel = os.path.relpath(target_file, start=source.parent).replace(os.sep, "/")
            href = urllib.parse.quote(rel, safe="/")
            if header and target_file.suffix == ".md":
                self.check_heading(source, target_file, header, lineno)
        return f"[{label}]({href}{anchor})"

    def check_heading(self, source: Path, target: Path, header: str, lineno: int) -> None:
        slug = slugify(header)
        count = self.headings_of(target).get(slug, 0)
        where = target.relative_to(self.root).as_posix()
        if count == 0:
            self.warn(source, lineno, f"heading '{header}' not found in {where}")
        elif count > 1:
            self.warn(
                source, lineno,
                f"heading '{header}' appears {count} times in {where}; "
                "the link points to the first one",
            )

    def convert_text_segment(self, segment: str, source: Path, lineno: int) -> str:
        for m in EMBED_RE.finditer(segment):
            self.warn(
                source, lineno,
                f"embed '![[{m.group(1)}]]' is not converted; use ![alt](path)",
            )

        def repl(m: re.Match) -> str:
            result = self.convert_link(m.group(1), source, lineno)
            self.converted += 1
            if self.dry_run:
                rel = source.relative_to(self.root).as_posix()
                print(f"{rel}:{lineno}: {m.group(0)} -> {result}")
            return result

        return WIKILINK_RE.sub(repl, segment)

    def convert_line(self, line: str, source: Path, lineno: int) -> str:
        out, pos = [], 0
        for code in INLINE_CODE_RE.finditer(line):
            out.append(self.convert_text_segment(line[pos:code.start()], source, lineno))
            out.append(code.group(0))
            pos = code.end()
        out.append(self.convert_text_segment(line[pos:], source, lineno))
        return "".join(out)

    def convert_file(self, path: Path) -> bool:
        original = path.read_bytes().decode("utf-8")
        lines = original.splitlines(keepends=True)
        start = split_front_matter(lines)
        result = lines[:start]
        fence: tuple[str, int] | None = None
        for i in range(start, len(lines)):
            line = lines[i]
            m = FENCE_RE.match(line)
            if m:
                marker = m.group(1)
                if fence is None:
                    fence = (marker[0], len(marker))
                elif marker[0] == fence[0] and len(marker) >= fence[1]:
                    fence = None
                result.append(line)
                continue
            if fence is not None:
                result.append(line)
            else:
                result.append(self.convert_line(line, path, i + 1))
        converted = "".join(result)
        if converted == original:
            return False
        if not self.dry_run:
            path.write_bytes(converted.encode("utf-8"))
        print(f"{'Would convert' if self.dry_run else 'Converted'} links in "
              f"{path.relative_to(self.root).as_posix()}")
        return True

    def run(self) -> None:
        for path in self.files:
            self.convert_file(path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--root", default=".", help="project root (default: .)")
    parser.add_argument("--dry-run", action="store_true",
                        help="print the conversions but do not modify any file")
    parser.add_argument("--strict", action="store_true",
                        help="exit with status 1 if any link could not be resolved")
    parser.add_argument("--skip-dir", action="append", default=[],
                        help="additional directory name to skip (repeatable)")
    args = parser.parse_args()

    root = Path(args.root)
    if not root.is_dir():
        print(f"error: {root} is not a directory", file=sys.stderr)
        return 2

    converter = Converter(root, DEFAULT_SKIP_DIRS | set(args.skip_dir), args.dry_run)
    converter.run()
    print(f"{converter.converted} wikilink(s) processed, "
          f"{converter.problems} warning(s).")
    return 1 if (args.strict and converter.problems) else 0


if __name__ == "__main__":
    sys.exit(main())
