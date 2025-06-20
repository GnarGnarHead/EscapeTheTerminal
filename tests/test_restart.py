import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from escape import Game


def test_restart_command(monkeypatch, capsys):
    game = Game()
    inputs = iter([
        'take access.key',
        'cd lab',
        'restart',
        'pwd',
        'inventory',
        'quit',
    ])
    monkeypatch.setattr('builtins.input', lambda _='': next(inputs))
    game.run()
    out = capsys.readouterr().out
    lines = out.splitlines()
    assert '/' in lines  # pwd at root
    assert 'Inventory is empty.' in out
    assert 'Goodbye' in out
