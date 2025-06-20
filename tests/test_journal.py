from escape import Game


def test_journal_add_and_list(capsys):
    game = Game()
    game._journal("add first note")
    game._journal("add second note")
    out = capsys.readouterr().out
    assert out.count("Note added.") == 2
    game._journal()
    out = capsys.readouterr().out
    assert "first note" in out
    assert "second note" in out


def test_journal_persistence(tmp_path):
    game = Game()
    game.save_file = tmp_path / "game.sav"
    game._journal("add remember this")
    game._save()

    new_game = Game()
    new_game.save_file = game.save_file
    new_game._load()
    assert new_game.journal == ["remember this"]

