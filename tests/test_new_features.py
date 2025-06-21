import os
import sys
import subprocess
from escape import Game

REPO_ROOT = os.path.dirname(os.path.dirname(__file__))
CMD = [sys.executable, '-m', 'escape']


def test_registry_allows_dynamic_command(monkeypatch, capsys):
    os.environ['ET_EXTRA_SEED'] = '42'
    game = Game()

    def dance(arg=""):
        game._output(f"Dancing {arg}")

    game.command_map['dance'] = lambda arg="": dance(arg)

    inputs = iter(['dance wildly', 'quit'])
    monkeypatch.setattr('builtins.input', lambda _='': next(inputs))
    game.run()
    out = capsys.readouterr().out
    assert 'Dancing wildly' in out
    assert 'Goodbye' in out


def test_talk_wrong_location(capsys):
    os.environ['ET_EXTRA_SEED'] = '99'
    game = Game()
    game._talk('daemon')
    out = capsys.readouterr().out
    assert 'There is no daemon here.' in out


def test_glitch_system_messages(capsys):
    os.environ['ET_EXTRA_SEED'] = '123'
    game = Game()
    game.glitch_mode = True
    for _ in range(6):
        game._output('test')
    out = capsys.readouterr().out
    import random
    msg3 = random.Random(3 * 42).choice([
        "-- SYSTEM CORRUPTION --",
        "** SIGNAL LOST **",
        "[memory anomaly]",
    ])
    msg6 = random.Random(6 * 42).choice([
        "-- SYSTEM CORRUPTION --",
        "** SIGNAL LOST **",
        "[memory anomaly]",
    ])
    assert msg3 in out
    assert msg6 in out


def test_load_missing_save_slot(tmp_path):
    env = os.environ.copy()
    env['ET_EXTRA_SEED'] = '321'
    env['PYTHONPATH'] = REPO_ROOT
    result = subprocess.run(
        CMD,
        input='load 9\nquit\n',
        text=True,
        capture_output=True,
        cwd=tmp_path,
        env=env,
    )
    assert 'No save file found.' in result.stdout
    assert 'Goodbye' in result.stdout


def test_glitch_thresholds_modify_fs(capsys):
    game = Game()
    game.glitch_mode = True
    for _ in range(5):
        game._output('tick')
    assert 'glitch.note' in game.fs['items']

    for _ in range(5):
        game._output('tick')
    assert 'glitch.note' not in game.fs['items']
    assert '(corrupted)' in game.fs['desc']

    for _ in range(5):
        game._output('tick')
    assert 'lab_glt' in game.fs['dirs']

    for _ in range(5):
        game._output('tick')
    import random
    expected = ['access.key', 'voice.log', 'door']
    rnd = random.Random(20)
    rnd.shuffle(expected)
    assert game.fs['items'] == expected

    for _ in range(5):
        game._output('tick')
    assert 'glitcher' in game.npc_locations
    assert '(fractured reality)' in game.fs['desc']


def test_alias_command(monkeypatch, capsys):
    game = Game()
    inputs = iter([
        'alias ll look',
        'll',
        'quit',
    ])
    monkeypatch.setattr('builtins.input', lambda _='': next(inputs))
    game.run()
    out = capsys.readouterr().out
    assert 'Alias ll -> look' in out
    assert 'dimly lit terminal' in out
    assert game.aliases['ll'] == 'look'
    assert 'Goodbye' in out


def test_alias_with_args(monkeypatch, capsys):
    game = Game()
    inputs = iter([
        'alias grab take',
        'grab access.key',
        'inventory',
        'quit',
    ])
    monkeypatch.setattr('builtins.input', lambda _='': next(inputs))
    game.run()
    out = capsys.readouterr().out
    assert 'Alias grab -> take' in out
    assert 'pick up the access.key' in out
    assert 'Inventory: access.key' in out
    assert 'Goodbye' in out


def test_unalias_command(monkeypatch, capsys):
    game = Game()
    inputs = iter([
        'alias ll look',
        'unalias ll',
        'll',
        'quit',
    ])
    monkeypatch.setattr('builtins.input', lambda _='': next(inputs))
    game.run()
    out = capsys.readouterr().out
    assert 'Alias ll -> look' in out
    assert 'Removed alias ll' in out
    assert 'Unknown command: ll' in out
    assert 'Goodbye' in out


def test_unalias_missing(monkeypatch, capsys):
    game = Game()
    inputs = iter([
        'unalias nope',
        'quit',
    ])
    monkeypatch.setattr('builtins.input', lambda _='': next(inputs))
    game.run()
    out = capsys.readouterr().out
    assert 'No such alias: nope' in out
    assert 'Goodbye' in out
