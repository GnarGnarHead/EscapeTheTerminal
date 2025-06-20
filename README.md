# EscapeTheTerminal
A retro cybertext adventure inspired by Philip K. Dick and William Gibson.

This project is a minimalist terminal game. For the long-term vision, see [VISIONDOCUMENT.md](VISIONDOCUMENT.md).

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
   The `use <item>` command lets you interact with objects in your inventory.
   Items can be discarded with `drop <item>`.
   Navigate the world as if it were a filesystem using `ls` to list the
   contents of the current room and `cd <dir>` to move between rooms.
   Use `cat <file>` to read narrative logs stored under the `data` directory.
   Use `save` to write your progress to `game.sav` and `load` to restore it.

## Running Tests
Tests require `pytest` and can be executed with:
```bash
pytest
```
