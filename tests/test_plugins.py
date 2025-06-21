import os
import sys
import subprocess
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


def test_zip_plugin(monkeypatch, capsys, tmp_path):
    plugin_dir = tmp_path / 'plugins'
    plugin_dir.mkdir()
    zip_path = plugin_dir / 'zipplug.zip'
    plugin_code = (
        "def hello(arg=\"\"):\n"
        "    game._output(\"Hello from zip\")\n\n"
        "if 'game' in globals():\n"
        "    game.command_map['hello'] = lambda arg=\"\": hello(arg)\n"
    )
    import zipfile
    with zipfile.ZipFile(zip_path, 'w') as zf:
        zf.writestr('zipplug.py', plugin_code)
    monkeypatch.setenv('ET_PLUGIN_PATH', str(plugin_dir))
    try:
        game = Game()
        inputs = iter(['hello', 'quit'])
        monkeypatch.setattr('builtins.input', lambda _='': next(inputs))
        game.run()
        out = capsys.readouterr().out
        assert 'Hello from zip' in out
        assert 'Goodbye' in out
    finally:
        zip_path.unlink(missing_ok=True)
        monkeypatch.delenv('ET_PLUGIN_PATH', raising=False)
        sys.modules.pop('zipplug', None)


def test_dance_plugin_loaded(monkeypatch, capsys):
    game = Game()
    inputs = iter(['dance happily', 'quit'])
    monkeypatch.setattr('builtins.input', lambda _='': next(inputs))
    game.run()
    out = capsys.readouterr().out
    assert 'Dancing happily' in out
    assert 'Goodbye' in out


def test_counter_plugin_state(monkeypatch, capsys, tmp_path):
    plugin_dir = tmp_path / 'plugins'
    plugin_dir.mkdir()
    plugin_path = plugin_dir / 'my_counter.py'
    plugin_code = (
        "counter = 0\n"
        "def counter_cmd(arg=\"\"):\n"
        "    global counter\n"
        "    counter += 1\n"
        "    game._output(f'Counter: {counter}')\n\n"
        "if 'game' in globals():\n"
        "    game.command_map['counter'] = lambda arg=\"\": counter_cmd(arg)\n"
    )
    plugin_path.write_text(plugin_code)
    monkeypatch.setenv('ET_PLUGIN_PATH', str(plugin_dir))
    try:
        game = Game()
        inputs = iter(['counter', 'counter', 'quit'])
        monkeypatch.setattr('builtins.input', lambda _='': next(inputs))
        game.run()
        out = capsys.readouterr().out.splitlines()
        assert 'Counter: 1' in out
        assert 'Counter: 2' in out
        assert 'Goodbye' in out[-1]
    finally:
        plugin_path.unlink(missing_ok=True)
        monkeypatch.delenv('ET_PLUGIN_PATH', raising=False)
        sys.modules.pop('my_counter', None)


def test_theme_plugin(monkeypatch, capsys):
    game = Game()
    assert 'theme' in game.command_map
    inputs = iter(['theme neon', 'quit'])
    monkeypatch.setattr('builtins.input', lambda _='': next(inputs))
    game.run()
    assert game.dir_color == '\x1b[92m'
    assert game.item_color == '\x1b[95m'


def test_theme_plugin_custom_codes(monkeypatch, capsys):
    game = Game()
    inputs = iter(['theme 32 31', 'quit'])
    monkeypatch.setattr('builtins.input', lambda _='': next(inputs))
    game.run()
    assert game.dir_color == '\x1b[32m'
    assert game.item_color == '\x1b[31m'


def test_puzzle_plugin(monkeypatch, capsys):
    game = Game()
    inputs = iter([
        'puzzle',
        'puzzle There is a secret message.',
        'quit',
    ])
    monkeypatch.setattr('builtins.input', lambda _='': next(inputs))
    game.run()
    out_lines = capsys.readouterr().out.splitlines()
    assert any('Decode this:' in line for line in out_lines)
    assert 'Correct! Puzzle solved.' in out_lines


def test_cli_plugin_path_flag(tmp_path):
    plugin_dir = tmp_path / 'mods'
    plugin_dir.mkdir()
    plugin_file = plugin_dir / 'cliplug.py'
    plugin_file.write_text(
        "def hi(arg=\"\"):\n    game._output('Hi via CLI')\n\n"
        "if 'game' in globals():\n    game.command_map['hi'] = lambda arg=\"\": hi(arg)\n"
    )

    env = os.environ.copy()
    env['PYTHONPATH'] = os.path.dirname(os.path.dirname(__file__))
    result = subprocess.run(
        [sys.executable, '-m', 'escape', '--plugin-path', str(plugin_dir)],
        input='hi\nquit\n',
        text=True,
        capture_output=True,
        env=env,
    )
    assert 'Hi via CLI' in result.stdout
    assert 'Goodbye' in result.stdout


def test_plugins_command_lists_builtins(monkeypatch, capsys):
    game = Game()
    inputs = iter(['plugins', 'quit'])
    monkeypatch.setattr('builtins.input', lambda _='': next(inputs))
    game.run()
    out_lines = capsys.readouterr().out.splitlines()
    expected = {
        'escape.plugins.counter',
        'escape.plugins.dance',
        'escape.plugins.puzzle',
        'escape.plugins.theme',
    }
    assert expected.issubset(set(out_lines))
