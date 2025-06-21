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
        "The dreamer flickers with digital noise, unstable yet alluring.", 2
    )

    result = subprocess.run(
        CMD,
        input='glitch\ncd dream\ncd npc\ntalk dreamer\n1\n1\nquit\n',
        text=True,
        capture_output=True,
    )
    assert expected in result.stdout
