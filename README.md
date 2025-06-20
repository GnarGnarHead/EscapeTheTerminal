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
3. Run the game using the console entry point or module:
   ```bash
   escape-terminal
   # or
   python -m escape
   ```
   Use `help` (or `h`) inside the game for available commands and `quit` (or `exit`) to exit.
   Common command aliases like `i`/`inv` for `inventory` and `look around` for `look` are also supported. You can also `look <dir>` to preview a subdirectory without entering it.

   **Core commands**
   - `look [dir]` / `look around` – describe the current room or a subdirectory
   - `take <item>` / `drop <item>` – manage inventory items
   - `inventory` / `i` / `inv` – show what you're carrying
   - `examine <item>` – get a closer look at an object
  - `use <item> [on <target>]` – interact with items (e.g. `use access.key on door` reveals hidden areas)
   - `ls` – list directories and items in the current location
   - `cd <dir>` – move between directories/rooms
   - `map` – display the directory tree from the current location
   - `cat <file>` – read narrative logs from `data/`
   - `decode mem.fragment` – combine the decoder with the memory fragment to reveal an escape code
   - `talk <npc>` – initiate conversation and choose numbered replies
   - `scan <dir>` – search a directory for hidden nodes
   - `hack <dir>` – attempt to unlock a scanned node
  - `grep <pattern> [file]` – search log files for matching text
  - `save [slot]` / `load [slot]` – write and restore progress. Without a slot the file `game.sav` is used, otherwise `game<slot>.sav`.
  - `glitch` – toggle glitch mode for scrambled descriptions. The longer it
    stays active the stronger the corruption becomes and occasional glitch
    messages may appear.
  - `color on` / `color off` / `color toggle` – enable, disable or toggle ANSI colors
  - `history` – display the commands you've entered this session
  - `journal` – view notes or `journal add <text>` to record a message
  - `sleep [reset|inc]` – fall asleep and enter the dream. Use `reset` to
    clear glitches or `inc` to deepen them
  - `alias <name> <command>` – create a custom shortcut
  - `unalias <name>` – remove a previously defined shortcut

  **Core files/items**
  - `access.key` – unlocks the hidden directory when used on the door
   - `voice.log` – whispers a clue when read
   - `mem.fragment` – a corrupted memory chunk found in `hidden/`
   - `treasure.txt` – reward text tucked away in `hidden/`
  - `decoder` – located in the `lab/` directory
  - `old.note` – stashed away in the `archive/` directory
  - `daemon.log` – consult the system daemon when read or used, found in `core/npc/`
  - `escape.code` – the deciphered sequence unlocked within the vault
  - `port.scanner` – enables hacking of network nodes, found in the `lab/`

   **Rooms**
   - `lab/` – a cluttered research area humming with equipment
  - `archive/` – dusty shelves of old backups and forgotten notes
  - `core/npc/` – a secluded nook where a daemon awaits interaction
  - `network/` – a tangle of digital links hiding a chain of nodes down to `node5`
  - `dream/oracle/` – an enigmatic hall where the oracle offers cryptic advice

## Running Tests
Tests are written with `pytest` and live under the `tests/` directory. After installing
the requirements, simply run `pytest` from the project root:
```bash
pytest
```
Use `pytest tests/test_basic.py::test_name` to execute an individual test during
development.
These tests also run automatically on GitHub via the workflow in
`.github/workflows/ci.yml` for Python 3.8 and 3.11.

## Procedural Directories
The game randomly adds extra subdirectories to several base areas on startup.
By default the `dream/`, `memory/` and `core/` directories each receive two or
three generated locations, sometimes containing unique items. Set the
`ET_EXTRA_SEED` environment variable before launching to make this generation
deterministic for reproducible testing or custom scenarios.
You can also set `ET_EXTRA_COUNT` to control exactly how many extra directories
are created under each base path.

## Autosave
Set the `ET_AUTOSAVE` environment variable to automatically write `game.sav`
after every successful command. This is handy for continuous progress backups or
automated testing.

## Custom Prompt
Set the `ET_PROMPT` environment variable to change the input prompt shown to
the player. The default prompt is `> `.

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

See [docs/NPC_DIALOG.md](docs/NPC_DIALOG.md) for the full file format. The helper
script `python -m escape.utils.validate_dialog <path>` checks dialog files for
common mistakes.

Modders can create additional files following this pattern and place their NPCs
in the game world by extending ``Game.npc_locations``.
The provided ``oracle.dialog`` shows a multi-stage conversation for an oracle
NPC located under ``dream/oracle/``.

## Plugins
Python files placed in ``escape/plugins/`` are discovered on startup. The game
scans this directory for ``*.py`` modules (ignoring names beginning with
``__``) and imports each one. Plugins are loaded inside ``Game._load_plugins``
which injects the active ``Game`` instance into each module before executing
it:

```python
for path in plugins_dir.glob("*.py"):
    if path.name.startswith("__"):
        continue
    module_name = f"escape.plugins.{path.stem}"
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        module.game = self  # expose the running game to the plugin
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
```

Every plugin module receives this ``game`` object via a global variable and can
register new commands by updating ``game.command_map`` during import. The
included ``dance.py`` plugin shows the recommended pattern:

```python
def dance(arg=""):
    game._output(f"Dancing {arg}" if arg else "Dancing")

# register the command on import
if 'game' in globals():
    game.command_map['dance'] = lambda arg="": dance(arg)
```

The ``game`` object exposes all of the engine internals so a plugin can do
virtually anything. This flexibility also means plugins execute arbitrary Python
code. Only enable plugins you trust, especially when distributing the game to
others.

## Custom Worlds
The starting filesystem, NPC locations and item descriptions are defined in
``escape/data/world.json``. Modify this file to reshape the world or provide a
completely new JSON file when instantiating ``Game`` using the ``world_file``
parameter. When running the CLI you can pass ``--world <file>`` to load an
alternate JSON world.
