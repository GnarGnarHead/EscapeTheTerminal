from escape import Game


def test_achievement_persistence(tmp_path):
    game = Game()
    game.save_file = tmp_path / "game.sav"
    game.unlock_achievement("first")
    game._save()

    new_game = Game()
    new_game.save_file = game.save_file
    new_game._load()
    assert new_game.achievements == ["first"]

