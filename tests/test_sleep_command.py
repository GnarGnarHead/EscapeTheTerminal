from escape import Game


def test_sleep_moves_to_dream(capsys):
    game = Game()
    game._sleep()
    capsys.readouterr()
    assert game.current == ['dream']


def test_sleep_resets_glitch():
    game = Game()
    game.glitch_steps = 5
    game._sleep('reset')
    assert game.glitch_steps == 0


def test_sleep_increments_glitch():
    game = Game()
    game._sleep('inc')
    assert game.glitch_steps == 1
