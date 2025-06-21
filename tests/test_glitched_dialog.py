import subprocess
import sys

CMD = [sys.executable, '-m', 'escape']


def test_dreamer_dialog_normal():
    result = subprocess.run(
        CMD,
        input='cd dream\ncd npc\ntalk dreamer\n1\n1\nquit\n',
        text=True,
        capture_output=True,
    )
    assert 'dreamer seems stable' in result.stdout


def test_dreamer_dialog_glitched():
    from escape import Game

    expected = Game()._glitch_text(
        "The dreamer flickers with digital noise.", 2
    )

    result = subprocess.run(
        CMD,
        input='glitch\ncd dream\ncd npc\ntalk dreamer\n1\n1\nquit\n',
        text=True,
        capture_output=True,
    )
    assert expected in result.stdout


def test_glitch_milestone_12_message(capsys):
    from escape import Game

    game = Game()
    game.glitch_mode = True
    for _ in range(11):
        game._output('tick')
    capsys.readouterr()
    game._output('tick')
    out = capsys.readouterr().out
    expected = game._glitch_text(
        "For a split second a directory named 'beyond/' blinks into existence then fades.",
        13,
    )
    assert expected in out


def test_glitch_milestone_18_message(capsys):
    from escape import Game

    game = Game()
    game.glitch_mode = True
    for _ in range(17):
        game._output('tick')
    capsys.readouterr()
    game._output('tick')
    out = capsys.readouterr().out
    expected = game._glitch_text(
        "A phantom file 'escape.exe' materializes before dissolving back into nothingness.",
        19,
    )
    assert expected in out
