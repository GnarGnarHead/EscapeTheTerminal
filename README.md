# EscapeTheTerminal
A retro cybertext adventure inspired by Philip K. Dick and William Gibson.

This project is a minimalist terminal game. For the long-term vision, see [VISIONDOCUMENT.md](VISIONDOCUMENT.md).
At a glance the game aims to mix **narrative computing** with familiar shell commands
to create a surreal hacking experience. Directories act as rooms, `ls` and `cd`
drive exploration, and commands like `use` or `glitch` advance the story in
unexpected ways.

## Setup
1. Install Python 3.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the game:
   ```bash
   python escape.py
   ```
   Use `help` (or `h`) inside the game for available commands and `quit` (or `exit`) to exit.
   Common command aliases like `i`/`inv` for `inventory` and `look around` for `look` are also supported.

   **Core commands**
   - `look` / `look around` – describe the current room
   - `take <item>` / `drop <item>` – manage inventory items
   - `inventory` / `i` / `inv` – show what you're carrying
   - `examine <item>` – get a closer look at an object
   - `use <item>` – interact with items (e.g. the `access.key` reveals hidden areas)
   - `ls` – list directories and items in the current location
   - `cd <dir>` – move between directories/rooms
   - `cat <file>` – read narrative logs from `data/`
   - `save` / `load` – write and restore your progress to `game.sav`
   - `glitch` – toggle glitch mode for scrambled descriptions

   **Core files/items**
   - `access.key` – unlocks the hidden directory when used
   - `voice.log` – whispers a clue when read
   - `mem.fragment` – a corrupted memory chunk found in `hidden/`
   - `treasure.txt` – reward text tucked away in `hidden/`
   - `decoder` – located in the `lab/` directory
   - `old.note` – stashed away in the `archive/` directory

   **Rooms**
   - `lab/` – a cluttered research area humming with equipment
   - `archive/` – dusty shelves of old backups and forgotten notes

## Running Tests
Tests are written with `pytest` and live under the `tests/` directory. After installing
the requirements, simply run `pytest` from the project root:
```bash
pytest
```
Use `pytest tests/test_basic.py::test_name` to execute an individual test during
development.
