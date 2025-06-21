from escape import Game


def test_stats_output_basic(capsys):
    game = Game()
    game._cd('lab')
    game._cd('..')
    game._take('access.key')
    capsys.readouterr()
    game._stats()
    out_lines = capsys.readouterr().out.splitlines()
    assert "Visited locations: 2" in out_lines
    assert "Items obtained: 1" in out_lines
    assert "Active quests: 1" in out_lines
    assert "Achievements unlocked: 0" in out_lines
    assert "Score: 0" in out_lines
