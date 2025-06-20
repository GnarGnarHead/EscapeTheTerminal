import os
import sys
from pathlib import Path

# Ensure local package is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from escape import Game


def test_temp_plugin_command(monkeypatch, capsys, tmp_path):
    plugin_dir = tmp_path / 'plugins'
    plugin_dir.mkdir()
    plugin_path = plugin_dir / 'temp_plugin.py'
    plugin_code = (
        "def hello(arg=\"\"):\n"
        "    game._output(\"Hello from plugin\")\n\n"
        "if 'game' in globals():\n"
        "    game.command_map['hello'] = lambda arg=\"\": hello(arg)\n"
    )
    plugin_path.write_text(plugin_code)
    monkeypatch.setenv('ET_PLUGIN_PATH', str(plugin_dir))
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
        monkeypatch.delenv('ET_PLUGIN_PATH', raising=False)
        sys.modules.pop('temp_plugin', None)


def test_dance_plugin_loaded(monkeypatch, capsys):
    game = Game()
    inputs = iter(['dance happily', 'quit'])
    monkeypatch.setattr('builtins.input', lambda _='': next(inputs))
    game.run()
    out = capsys.readouterr().out
    assert 'Dancing happily' in out
    assert 'Goodbye' in out
