# Plugin Development

EscapeTheTerminal supports optional plugins that extend the game with new commands or behaviour. Plugins are discovered at startup and may live either in the built in `escape/plugins/` directory or in additional paths specified through the `ET_PLUGIN_PATH` environment variable.

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

This would load plugins from ``/path/to/mods`` and ``/other/plugins`` in addition to the bundled ones.

Plugins execute arbitrary Python code so only use plugins from trusted sources.


