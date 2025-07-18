# Plugin Development

EscapeTheTerminal supports optional plugins that extend the game with new commands or behaviour. Plugins are discovered at startup and may live either in the built in `escape/plugins/` directory or in additional paths specified through the `ET_PLUGIN_PATH` environment variable.

The same paths can be provided on the command line using the `--plugin-path` option when starting the game.

``ET_PLUGIN_PATH`` may contain one or more directories separated by the operating system path separator (``:`` on Unix-like systems, ``;`` on Windows). Each directory is scanned for ``*.py`` files and ``*.zip`` archives and everything found is imported as a module.

## Simple ``.py`` Plugin

Create a Python file inside a plugin directory and register commands as soon as the module is imported. Every plugin receives the running ``game`` instance as a global variable.

```python
# greet.py

def greet(name=""):
    game._output(f"Greetings, {name}!" if name else "Greetings!")

if 'game' in globals():
    game.command_map['greet'] = lambda arg="": greet(arg)
```

Place ``greet.py`` under ``escape/plugins/`` or a directory listed in ``ET_PLUGIN_PATH`` and launch the game. The ``greet`` command will be available immediately.

The project also includes a small stateful example named ``counter.py``. Each
time you run the ``counter`` command the number it prints increases. This shows
that plugins can maintain their own module state between invocations.

## ``.zip`` Plugin Example

Plugins can also be distributed as zip archives. The archive should contain a single Python module. The name of the zip file becomes the module name when loaded.

```text
hello.zip
    hello.py
```

`hello.py` could look like:

```python
def hello(arg=""):
    game._output("Hello from zip")

if 'game' in globals():
    game.command_map['hello'] = lambda arg="": hello(arg)
```

Put ``hello.zip`` in a plugin directory and run the game to use the ``hello`` command.

## Loading Plugins

On startup the game imports all plugins from ``escape/plugins/``. If ``ET_PLUGIN_PATH`` is defined, its directories are processed as well. For example:

```bash
ET_PLUGIN_PATH=/path/to/mods:/other/plugins escape-terminal
```

The same result can be achieved with the command line flag:

```bash
escape-terminal --plugin-path /path/to/mods:/other/plugins
```

This would load plugins from ``/path/to/mods`` and ``/other/plugins`` in addition to the bundled ones.

Plugins execute arbitrary Python code so only use plugins from trusted sources.

## Built-in Theme Plugin

The repository ships with a small ``theme.py`` plugin located in
``escape/plugins/``. It loads automatically and adds a ``theme`` command for
changing the highlight colors at runtime.

```
theme dark   # blue directories, magenta items
theme mono   # monochrome output
theme neon   # bright green directories and magenta items
theme 32 35  # use custom ANSI codes
```

Running one of these commands sets ``game.dir_color`` and ``game.item_color`` to
predefined or custom ANSI codes. When the argument does not match a preset,
provide two color codes (as numbers understood by the terminal) to set the
directory and item colors explicitly.


## Built-in Puzzle Plugin

A second bundled plugin named `puzzle.py` offers a small code-breaking riddle. Run `puzzle` without arguments to see the encoded phrase and pass your decoded answer to solve it. The module remembers if you solved the puzzle so subsequent runs simply report that it is already complete.

## Built-in Cipher Plugin

The `cipher.py` plugin presents a short ROT13 message. Run `cipher` to display the scrambled text and supply the decoded phrase to complete the challenge.

## Built-in Riddle Plugin

The `riddle.py` module presents a short question the first time you run `riddle`. Run the command again with your guess and it will tell you if you are correct.

## Built-in Weather Plugin

The `weather.py` plugin prints a random short forecast whenever you run `weather`.
