import builtins
from escape import Game


def test_archivist_trust_increase(monkeypatch, capsys):
    game = Game()
    game._cd('memory')
    game._take('flashback.log')
    game._cd('npc')
    inputs = iter(['1', '1', '1', '1', '1', '1'])
    monkeypatch.setattr('builtins.input', lambda _='': next(inputs))
    # first conversation
    game._talk('archivist')
    capsys.readouterr()
    # second conversation - choose trust option
    game._talk('archivist')
    capsys.readouterr()
    assert game.npc_trust.get('archivist', 0) == 1
    # third conversation - trust gated line should appear
    game._talk('archivist')
    out = capsys.readouterr().out
    assert 'faded index code' in out
    # give the log and gain more trust
    game._give('flashback.log')
    # fourth conversation reaches the waiting stage
    game._talk('archivist')
    capsys.readouterr()
    # fifth conversation - choose discuss log to gain more trust
    game._talk('archivist')
    capsys.readouterr()
    assert game.npc_trust.get('archivist', 0) == 2
    # sixth conversation - new line unlocked by high trust
    game._talk('archivist')
    out = capsys.readouterr().out
    assert 'hidden backup archive' in out


def test_daemon_trust_branch(monkeypatch, capsys):
    game = Game()
    game._cd('core')
    game._cd('npc')
    # first conversation requires two selections
    inputs = iter(['1', '1'])
    monkeypatch.setattr('builtins.input', lambda _='': next(inputs))
    game._talk('daemon')
    capsys.readouterr()

    # second conversation
    inputs = iter(['1'])
    monkeypatch.setattr('builtins.input', lambda _='': next(inputs))
    game._talk('daemon')
    capsys.readouterr()

    # third conversation - choose trust option
    inputs = iter(['1'])
    monkeypatch.setattr('builtins.input', lambda _='': next(inputs))
    game._talk('daemon')
    capsys.readouterr()

    # trust gated line appears on fourth talk
    inputs = iter(['1'])
    monkeypatch.setattr('builtins.input', lambda _='': next(inputs))
    game._talk('daemon')
    out = capsys.readouterr().out
    assert 'daemon grants you access to hidden protocols' in out.lower()

