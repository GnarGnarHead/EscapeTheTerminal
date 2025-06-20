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


def test_sysop_polite_branch():
    result = subprocess.run(
        [sys.executable, SCRIPT],
        input='cd core\ncd npc\ntalk sysop\n1\ntalk sysop\n1\nquit\n',
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert 'sysop glances over' in out
    assert 'nods at your respect' in out
    assert 'welcomes your return' in out
    assert 'glitch' in out
    assert 'Goodbye' in out


def test_wanderer_helped_branch():
    result = subprocess.run(
        [sys.executable, SCRIPT],
        input='cd dream\ncd npc\ntalk wanderer\n2\ntalk wanderer\n1\nquit\n',
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert 'weary wanderer drifts' in out
    assert 'shares a secret path' in out
    assert 'Paths shift with each reboot' in out
    assert 'Goodbye' in out


def test_sysop_rude_branch():
    result = subprocess.run(
        [sys.executable, SCRIPT],
        input='cd core\ncd npc\ntalk sysop\n2\ntalk sysop\n1\nquit\n',
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert 'sysop glances over' in out
    assert 'scowls at your tone' in out
    assert 'folds their arms warily' in out
    assert 'glitch' in out
    assert 'Goodbye' in out


def test_wanderer_ignored_branch():
    result = subprocess.run(
        [sys.executable, SCRIPT],
        input='cd dream\ncd npc\ntalk wanderer\n1\ntalk wanderer\n1\nquit\n',
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert 'weary wanderer drifts' in out
    assert 'barely notices you' in out
    assert 'Paths shift with each reboot' in out
    assert 'Goodbye' in out
