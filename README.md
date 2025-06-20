# EscapeTheTerminal
A retro cybertext adventure inspired by Philip K. Dick and William Gibson.

This project is a minimalist terminal game. For the long-term vision, see [VISIONDOCUMENT.md](VISIONDOCUMENT.md).
At a glance the game aims to mix **narrative computing** with familiar shell commands
to create a surreal hacking experience. Directories act as rooms, `ls` and `cd`
drive exploration, and commands like `use` or `glitch` advance the story in
unexpected ways.

## Setup
1. Install Python 3.8 or higher.
2. Install the project in editable mode (including optional test extras):
   ```bash
   pip install -e '.[test]'
   ```
3. Run the game using the console entry point:
   ```bash
   escape-terminal
   ```
   Use `help` (or `h`) inside the game for available commands and `quit` (or `exit`) to exit.
   Common command aliases like `i`/`inv` for `inventory` and `look around` for `look` are also supported.

   **Core commands**
   - `look` / `look around` – describe the current room
   - `take <item>` / `drop <item>` – manage inventory items
   - `inventory` / `i` / `inv` – show what you're carrying
   - `examine <item>` – get a closer look at an object
  - `use <item> [on <target>]` – interact with items (e.g. `use access.key on door` reveals hidden areas)
   - `ls` – list directories and items in the current location
   - `cd <dir>` – move between directories/rooms
   - `cat <file>` – read narrative logs from `data/`
   - `talk <npc>` – initiate conversation and choose numbered replies
  - `save [slot]` / `load [slot]` – write and restore progress. Without a slot the file `game.sav` is used, otherwise `game<slot>.sav`.
  - `glitch` – toggle glitch mode for scrambled descriptions. The longer it
    stays active the stronger the corruption becomes and occasional glitch
    messages may appear.

   **Core files/items**
  - `access.key` – unlocks the hidden directory when used on the door
   - `voice.log` – whispers a clue when read
   - `mem.fragment` – a corrupted memory chunk found in `hidden/`
   - `treasure.txt` – reward text tucked away in `hidden/`
  - `decoder` – located in the `lab/` directory
  - `old.note` – stashed away in the `archive/` directory
  - `daemon.log` – consult the system daemon when read or used, found in `core/npc/`

   **Rooms**
   - `lab/` – a cluttered research area humming with equipment
  - `archive/` – dusty shelves of old backups and forgotten notes
  - `core/npc/` – a secluded nook where a daemon awaits interaction

## Running Tests
Tests are written with `pytest` and live under the `tests/` directory. After installing
the requirements, simply run `pytest` from the project root:
```bash
pytest
```
Use `pytest tests/test_basic.py::test_name` to execute an individual test during
development.

## Command Registry
Commands are routed through the ``Game.command_map`` dictionary. Each command
string or alias maps to a handler method. When adding a new command simply
register it in ``command_map`` with a callable that accepts the raw argument
string. The main loop will pass any text following the command name to the
handler automatically.

## Creating NPC Dialogs
NPC conversations are stored under ``data/npc`` using the naming scheme
``<name>.dialog``. The ``talk <name>`` command will load the matching file if the
player is in the correct directory for that NPC. Lines beginning with ``>`` are
treated as simple menu options. They appear as a numbered list and you select a
reply by typing its number. A minimal ``dreamer.dialog`` might look like:

```
The dreamer watches you closely.
> Ask about escape
> Ask about dreams
```

Modders can create additional files following this pattern and place their NPCs
in the game world by extending ``Game.npc_locations``.
