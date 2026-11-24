Helium Engine is a solo-led project with a specific vision of how mechanics fit together. Because of that, any undiscussed core-related changes are dismissed.

If you want to contribute with:

- Typos, readability and formatting fixes - feel free to open a pull request directly
- Core design changes or new mechanics - open a GitHub Issue or reach out on discord `vitamingaming` to discuss it. Once consensus is reached, make a PR to implement it

All accepted contributors will be included in credits in releases of documentation.

# How the repository is organized

All pages are md files in the root of the repository. Drawings are in `Drawings/` folder: each one is `.excalidraw.md` (the drawing itself, made with Obsidian Excalidraw plugin) and `.excalidraw.svg` (exported picture). Pages use the svg, so if you change a drawing, commit both files.

Site is configured in `zensical.toml`, new page has to be added to `nav` there to appear in the menu. On every push to `main` GitHub Actions builds the site with Zensical and puts it on GitHub Pages.

# Wikilinks

> Important note for contributors about wikilinks
> 
> This project is built using Obsidian, therefore originally its using wikilinks `[[link]]`. Since Zensical does **not** natively support wikilinks, on deployment stage there's converter script (`scripts/convertWikilinks.py`) that converts wikilinks into internal relative links `[text](link)` for Zensical to work with. For contributors, this means that they **may** use wikilinks for mentioning different pages, but importantly, they can **not** use wikilinks embedding `![[link]]` and must use basic link embedding `![text](link)`.

Supported wikilinks are `[[Page]]`, `[[Page|text]]`, `[[Page#Heading]]`, `[[Page#Heading|text]]` and `[[#Heading]]`. Inside tables write the separator as `\|`, otherwise Obsidian and Markdown tables break. Block references `[[Page#^id]]` are not supported. Also Obsidian image size like `![text|300](link)` doesnt work in Zensical, size is just ignored.

The script rewrites files, so dont run it on your Obsidian vault. It is meant for deployment only.

# Unfinished parts

Pages and sections that are not done yet have `[todo: ...]` note at the start. If you finish a section, remove its note, otherwise leave it.

# Pull requests

Keep one PR for one topic and say what you changed and why. If it changes mechanics, link the issue where it was discussed. After you open PR, check that the build in GitHub Actions passes, if it fails then most likely something is wrong with a link.

# License

By contributing you agree that your work is licensed under the same license as the engine, Creative Commons Attribution 4.0 (CC BY 4.0).