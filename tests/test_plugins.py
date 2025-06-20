import os
import sys
from pathlib import Path

# Ensure local package is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from escape import Game


def test_temp_plugin_command(monkeypatch, capsys):
    plugin_path = (
        Path(__file__).resolve().parent.parent
        / 'escape'
        / 'plugins'
        / 'temp_plugin.py'
    )
    plugin_code = (
        "def hello(arg=\"\"):\n"
        "    game._output(\"Hello from plugin\")\n\n"
        "if 'game' in globals():\n"
        "    game.command_map['hello'] = lambda arg=\"\": hello(arg)\n"
    )
    plugin_path.write_text(plugin_code)
    try:
        game = Game()
        inputs = iter(['hello', 'quit'])
        monkeypatch.setattr('builtins.input', lambda _='': next(inputs))
        game.run()
        out = capsys.readouterr().out
        assert 'Hello from plugin' in out
        assert 'Goodbye' in out
    finally:
        plugin_path.unlink(missing_ok=True)
        sys.modules.pop('escape.plugins.temp_plugin', None)
