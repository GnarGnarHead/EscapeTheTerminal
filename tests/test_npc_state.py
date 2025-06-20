import subprocess
import sys
import os

SCRIPT = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'escape.py')


def test_daemon_follow_up():
    result = subprocess.run(
        [sys.executable, SCRIPT],
        input='cd core\ncd npc\ntalk daemon\n1\n1\ntalk daemon\n1\nquit\n',
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert 'acknowledges your presence' in out
    assert 'flickers, recognizing you from before' in out
    assert 'I already mentioned decoding the fragment' in out
    assert 'Goodbye' in out


def test_dreamer_follow_up():
    result = subprocess.run(
        [sys.executable, SCRIPT],
        input='cd dream\ncd npc\ntalk dreamer\n1\n2\ntalk dreamer\n1\nquit\n',
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert 'dreamer watches you closely' in out
    assert 'nods knowingly this time' in out
    assert 'Trust the path the fragment reveals' in out
    assert 'Goodbye' in out

