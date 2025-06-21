from escape import Game


def test_give_success(monkeypatch, capsys):
    game = Game()
    # acquire item
    game._cd('dream')
    game._take('lucid.note')
    game._cd('..')
    game._cd('core')
    game._cd('npc')
    inputs = iter(['1'])
    monkeypatch.setattr('builtins.input', lambda _='': next(inputs))
    game._talk('mentor')
    capsys.readouterr()
    game._give('lucid.note')
    assert 'lucid.note' not in game.inventory
    inputs = iter(['1'])
    monkeypatch.setattr('builtins.input', lambda _='': next(inputs))
    game._talk('mentor')
    out = capsys.readouterr().out
    assert 'Demonstrate lucid techniques' in out


def test_give_no_active_npc(capsys):
    game = Game()
    game.inventory.append('lucid.note')
    game._give('lucid.note')
    out = capsys.readouterr().out
    assert 'There is no one here to give that to.' in out
    assert 'lucid.note' in game.inventory


def test_give_item_missing(monkeypatch, capsys):
    game = Game()
    # talk to mentor so an NPC is active
    game._cd('core')
    game._cd('npc')
    inputs = iter(['1'])
    monkeypatch.setattr('builtins.input', lambda _='': next(inputs))
    game._talk('mentor')
    capsys.readouterr()
    game._give('lucid.note')
    out = capsys.readouterr().out
    assert 'You do not have lucid.note to give.' in out


def test_give_usage(monkeypatch, capsys):
    game = Game()
    game.inventory.append('lucid.note')
    game._cd('core')
    game._cd('npc')
    inputs = iter(['1'])
    monkeypatch.setattr('builtins.input', lambda _='': next(inputs))
    game._talk('mentor')
    capsys.readouterr()
    game._give('')
    out = capsys.readouterr().out
    assert 'Usage: give <item>' in out
