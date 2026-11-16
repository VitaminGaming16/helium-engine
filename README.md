# Helium Engine
Helium engine is lightweight TTRPG system engine. Word "engine" means that its just foundation, you cant play engine itself but rather build your own system on top of it. It serves as DnD alternative for more opportunities for dynamic fights, better social interactions and most importantly less homebrew (changing already existing mechanics) but actual system building. Note that while Helium Engine aims to grant all these pros to systems built on top of it, it still depends on exact system implementation, DM and players.
Latest version is hosted on [GitHub Pages](https://vitamingaming16.github.io/helium-engine/)

# What this repository is for
Repository was made for easier collaboration, version tracking and overall convenience, as well as github pages hosting. Online wiki is built on Zensical that converts md files into websites and hosted by GitHub Pages for free.

# Current state
Right now its in very early development. Current to-do list:
- [x] Inventory system
- [x] Character sheets
- [x] Github Pages & Zensical
- [ ] Tags library
- [ ] Initiative
- [ ] Combat system
- [ ] Social interactions
- [ ] Off-camera activities (time skips, etc)
- [ ] Life resources (hp, sleep, food)
- [ ] First pdf playbook release

# How to contribute
Since its creativity child of VitaminGaming16, its not possible to let anything be changed by anyone. Right now, Helium Engine is solo-led design project with a specific vision how mechanics fit or should fit together. Because of that, any undiscussed core-related changes are dismissed.

If you want to contribute with:
- Typos, readability and formatting fixes - feel free to open a pull request directly
- Core design changes or new mechanics - open a GitHub Issue or reach out on discord `vitamingaming` to discuss it. Once consensus made, make PR to implement
All accepted contributors will be included in credits in releases of playbook

>[!important] Important note for contributors about wikilinks
>This project is built using Obsidian, therefore originally its using wikilinks `[[link]]`. Since Zensical does **not** natively support wikilinks, on deployment stage there's converter script that converts wikilinks into basic external links `[text](link)` for Zensical to work with. For contributors, this means that they **may** use wikilinks for mentioning different pages, but importantly, they can **not** use wikilinks embedding `![[link]]` and must use basic link embedding `![text](link)`.

# License
This TTRPG engine is licensed under Creative Commons CC-BY 4.0.