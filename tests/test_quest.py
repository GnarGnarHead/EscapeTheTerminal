from escape import Game


def test_quest_add_and_list(capsys):
    game = Game()
    game._quest("add find treasure")
    game._quest("add talk to mentor")
    out = capsys.readouterr().out
    assert out.count("Quest added.") == 2
    game._quest()
    out = capsys.readouterr().out
    assert "1. find treasure" in out
    assert "2. talk to mentor" in out


def test_quest_persistence(tmp_path):
    game = Game()
    game.save_file = tmp_path / "game.sav"
    game._quest("add escape the terminal")
    game._save()

    new_game = Game()
    new_game.save_file = game.save_file
    new_game._load()
    assert new_game.quests == ["escape the terminal"]

