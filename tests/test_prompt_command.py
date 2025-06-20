from escape import Game


def test_prompt_set_and_show(capsys):
    game = Game()
    game._prompt('>>> ')
    out = capsys.readouterr().out
    assert 'Prompt set to >>>' in out
    assert game.prompt == '>>> '
    game._prompt('')
    out = capsys.readouterr().out
    assert out.strip() == '>>>'
