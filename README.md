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
   Run ``escape-terminal --version`` to print the installed version and exit.

   **Core commands**
   - `look [dir]` / `look around` – describe the current room or a subdirectory
  - `take <item>` / `drop <item>` / `give <item>` – manage inventory and hand requested items to NPCs
   - `inventory` / `i` / `inv` – show what you're carrying
   - `examine <item>` – get a closer look at an object
  - `use <item> [on <target>]` – interact with items (e.g. `use access.key on door` reveals hidden areas)
   - `ls` – list directories and items in the current location
   - `cd <dir>` – move between directories/rooms
   - `map` – display the directory tree from the current location
  - `cat <file>` – read narrative logs from `data/`
  - `decode mem.fragment` – combine the decoder with the memory fragment to reveal an escape code
  - `combine <item1> <item2>` – craft a new item when a valid recipe exists
  - `talk <npc>` – initiate conversation and choose numbered replies
   - `scan <dir>` – search a directory for hidden nodes
   - `hack <dir>` – attempt to unlock a scanned node
  - `grep <pattern> [file]` – search log files for matching text
  - `save [slot]` / `load [slot]` – write and restore progress. Without a slot the file `game.sav` is used, otherwise `game<slot>.sav`.
  - `glitch` – toggle glitch mode for scrambled descriptions. The longer it
    stays active the stronger the corruption becomes and occasional glitch
    messages may appear.
    Special messages trigger at steps 12 and 18, hinting at a fleeting directory or phantom file.
  - `color on` / `color off` / `color toggle` – enable, disable or toggle ANSI colors
  - `prompt [text]` – show or change the input prompt
  - `history` – display the commands you've entered this session
  - `achievements` – list any achievements you've unlocked
  - `man <command>` – show the manual page for a command
  - `journal` – view notes or `journal add <text>` to record a message
  - `quest` – list quests or `quest add <text>` / `quest complete <id>`
    (quests can span multiple NPCs and progress through item exchanges)
  - `sleep [reset|inc]` – fall asleep and enter the dream. Use `reset` to
    clear glitches or `inc` to deepen them
  - `score` – display your current score
  - `stats` – show counts of visited locations and items collected
  - `restart` – reset the game while keeping color settings
  - `alias <name> <command>` – create a custom shortcut
  - `unalias <name>` – remove a previously defined shortcut
  - `plugins` – list loaded plugin modules

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
  - `loop.code` – resets reality and unlocks the optional void quest
  - `test.script` – an experimental file tucked away in the `sandbox/` directory

   **Rooms**
   - `lab/` – a cluttered research area humming with equipment
  - `archive/` – dusty shelves of old backups and forgotten notes
  - `core/npc/` – a secluded nook where a daemon awaits interaction
  - `network/` – a tangle of digital links hiding a chain of nodes down to `node7`
  - `sandbox/` – an isolated test area for trying new commands
  - `sandbox/npc/` – meet the sandboxer for tips on experimentation
  - `dream/oracle/` – an enigmatic hall where the oracle offers cryptic advice
  - `dream/tech_lab/` – home to the technomancer and advanced glitch research

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
are created under each base path. The same seed can be supplied on the command
line via ``--seed <num>`` and the count via ``--extra-count <num>``.

## Autosave
Set the `ET_AUTOSAVE` environment variable to automatically write `game.sav`
after every successful command. This is handy for continuous progress backups or
automated testing. Running ``escape-terminal --autosave`` enables the same
behavior without setting the environment variable.

`ET_SAVE_DIR` can be set to control where save files are stored. When unset,
files are saved to the current working directory.

## Custom Prompt
Set the `ET_PROMPT` environment variable to change the input prompt shown to
the player. The default prompt is `> `. You can also pass ``--prompt <text>`` on
the command line or use the in-game `prompt <text>` command.

## Color Customization
Set `ET_COLOR=1` to start the game with ANSI colors enabled. You can override
the highlight colors by defining `ET_COLOR_ITEM` and `ET_COLOR_DIR` with numeric
ANSI codes (e.g. `35` for magenta, `32` for green). These values control the
colors used for items and directories respectively.

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

See [docs/NPC_DIALOG.md](docs/NPC_DIALOG.md) for the full file format. Dialog
files can be checked for mistakes with the convenience command
`validate-dialog <path>` or by running the underlying module directly via
`python -m escape.utils.validate_dialog <path>`.
Dialog files committed under `escape/data/npc` are automatically validated in
the CI workflow.

Modders can create additional files following this pattern and place their NPCs
in the game world by extending ``Game.npc_locations``.
The provided ``oracle.dialog`` shows a multi-stage conversation for an oracle
NPC located under ``dream/oracle/``. A more experimental Technomancer can be
found within ``dream/tech_lab/``.

Cross-NPC quests let conversations hand off objectives between characters. An
NPC might ask you to deliver an item or speak with someone else before they
reveal more dialog. Use ``give <item>`` after talking to them to hand over what
they want and progress the shared quest chain.

Triggering the ``loop.code`` found in the runtime directory restarts the world
and unlocks a hidden ``void`` area where the wanderer offers additional insight.

## Plugins
See [docs/PLUGIN_DEVELOPMENT.md](docs/PLUGIN_DEVELOPMENT.md) for a full guide on creating and loading plugins.

Python files placed in ``escape/plugins/`` are discovered on startup. The game
scans this directory for ``*.py`` modules (ignoring names beginning with
``__``) and imports each one. Plugins are loaded inside ``Game._load_plugins``
which injects the active ``Game`` instance into each module before executing
it. Plugin directories may also contain ``*.zip`` archives. Each archive is
treated as a module named after the zip file and loaded via
``zipimport.zipimporter``:

You can add additional plugin directories by setting the `ET_PLUGIN_PATH` environment variable to one or more paths separated by the system path separator.
The same value can be supplied on the command line with `--plugin-path`.


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

The repository includes a few example plugins that are loaded automatically.
Run ``theme dark`` or ``theme neon`` to change the directory and item colors at
runtime, or try ``puzzle``, ``cipher``, ``riddle`` or ``weather`` for small
interactive extras.

Example ``cipher`` usage::

    cipher
    cipher You found a secret decoder.

## Custom Worlds
The starting filesystem, NPC locations and item descriptions are defined in
``escape/data/world.json``. Modify this file to reshape the world or provide a
completely new JSON file when instantiating ``Game`` using the ``world_file``
parameter. When running the CLI you can pass ``--world <file>`` to load an
alternate JSON world.

## Achievements
Certain actions unlock persistent achievements stored in ``Game.achievements``.
Use ``Game.unlock_achievement(name)`` to record one and ``Game.list_achievements``
to retrieve the list. The mem.fragment decode and unlocking the ``runtime`` node
award achievements out of the box. Achievements are saved along with other game
state when using the ``save`` and ``load`` commands. Inside the game you can run
the ``achievements`` command to display any that have been unlocked.
See [docs/GAME_MECHANICS.md](docs/GAME_MECHANICS.md) for details on scoring and
the restart command.

## Emotional Feedback
Reading certain memory logs now changes your avatar's mood. The current
`emotion_state` starts as `confused` and may become `alarmed` or `hopeful`
when key memories surface. Whenever this state changes a short thought like
`(You feel hopeful.)` is printed before the next line of output.
