import builtins
from escape import Game


def test_daemon_additional_section(monkeypatch, capsys):
    game = Game()
    game.npc_global_flags['decoded'] = True
    game.npc_global_flags['runtime'] = True
    game._cd('core')
    game._cd('npc')
    inputs = iter(['1', '1', '1', '1', '1'])
    monkeypatch.setattr('builtins.input', lambda _='': next(inputs))
    for _ in range(6):
        game._talk('daemon')
    out = capsys.readouterr().out
    assert "voice fades as it awaits further directives" in out


def test_dreamer_additional_section(monkeypatch, capsys):
    game = Game()
    game.npc_global_flags['decoded'] = True
    game.npc_global_flags['runtime'] = True
    game._cd('dream')
    game._cd('npc')
    inputs = iter(['1', '1', '1'])
    monkeypatch.setattr('builtins.input', lambda _='': next(inputs))
    for _ in range(4):
        game._talk('dreamer')
    out = capsys.readouterr().out
    assert "dream dims, leaving you in quiet contemplation." in out
