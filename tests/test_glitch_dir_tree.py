from escape import Game


def test_glitch_tree_added_and_removed():
    game = Game()
    assert 'glitch_root' not in game.fs['dirs']

    game._toggle_glitch()
    assert 'glitch_root' in game.fs['dirs']
    glitch = game.fs['dirs']['glitch_root']
    assert '.ghost' in glitch['items']
    assert 'false' in glitch['dirs']
    assert 'root' in glitch['dirs']['false']['items']

    game._toggle_glitch()
    assert 'glitch_root' not in game.fs['dirs']
