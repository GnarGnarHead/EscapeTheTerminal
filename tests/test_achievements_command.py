from escape import Game


def test_achievements_command_lists_unlocked(capsys):
    game = Game()
    game.unlock_achievement("first")
    game.command_map["achievements"]()
    out = capsys.readouterr().out
    assert "first" in out
