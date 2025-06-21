import subprocess
import sys
import os
from escape import Game

REPO_ROOT = os.path.dirname(os.path.dirname(__file__))
CMD = [sys.executable, '-m', 'escape']


def test_sage_first_and_second_stage():
    result = subprocess.run(
        CMD,
        input='cd archive\ncd npc\ntalk sage\n1\ntalk sage\n1\nquit\n',
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert 'sage sits quietly' in out
    assert '1. Seek wisdom' in out
    assert 'Ask about the dreamer' in out
    assert 'Patience reveals hidden truths.' in out
    assert 'sage smiles gently at your approach' in out
    assert 'Knowledge flows to those who listen.' in out
    assert 'Goodbye' in out


def test_sage_skeptical_after_repeated_talks(monkeypatch, capsys):
    game = Game()
    game._cd('archive')
    game._cd('npc')
    # first conversation - demand secrets
    inputs = iter(['2'])
    monkeypatch.setattr('builtins.input', lambda _='': next(inputs))
    game._talk('sage')
    capsys.readouterr()

    # second conversation - ask about escape
    inputs = iter(['1'])
    monkeypatch.setattr('builtins.input', lambda _='': next(inputs))
    game._talk('sage')
    capsys.readouterr()

    # third conversation - offer thanks
    inputs = iter(['1'])
    monkeypatch.setattr('builtins.input', lambda _='': next(inputs))
    game._talk('sage')
    out = capsys.readouterr().out
    assert 'delete these archives' in out or 'fork them' in out

