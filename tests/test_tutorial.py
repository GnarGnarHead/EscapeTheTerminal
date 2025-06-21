import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from escape import Game


def test_tutorial_outputs_steps(monkeypatch, capsys):
    game = Game()
    inputs = iter([
        'tutorial',
        'quit',
    ])
    monkeypatch.setattr('builtins.input', lambda _='': next(inputs))
    game.run()
    out = capsys.readouterr().out
    assert 'Tutorial:' in out
    assert 'Move using' in out
    assert 'Take an item' in out
    assert 'glitch' in out
    assert 'scan' in out
    assert 'hack' in out
    assert 'Goodbye' in out
