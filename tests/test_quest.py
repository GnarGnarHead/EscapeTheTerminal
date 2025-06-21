from escape import Game


def test_quest_add_and_list(capsys):
    game = Game()
    game._quest("add find treasure")
    game._quest("add talk to mentor")
    out = capsys.readouterr().out
    assert out.count("Quest added.") == 2
    game._quest()
    out_lines = capsys.readouterr().out.splitlines()
    assert any("find treasure" in line for line in out_lines)
    assert any("talk to mentor" in line for line in out_lines)


def test_quest_persistence(tmp_path):
    game = Game()
    game.save_file = tmp_path / "game.sav"
    game._quest("add escape the terminal")
    game._save()

    new_game = Game()
    new_game.save_file = game.save_file
    new_game._load()
    assert new_game.quests == ["Recover your lost memory", "escape the terminal"]

