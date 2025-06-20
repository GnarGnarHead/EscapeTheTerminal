import subprocess
import sys
import os

REPO_ROOT = os.path.dirname(os.path.dirname(__file__))
CMD = [sys.executable, '-m', 'escape']


def test_take_drop_after_network_puzzle():
    result = subprocess.run(
        CMD,
        input=(
            'cd lab\n'
            'take port.scanner\n'
            'cd ..\n'
            'scan network\n'
            'hack network\n'
            'take access.key\n'
            'drop access.key\n'
            'ls\n'
            'quit\n'
        ),
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert 'You pick up the access.key' in out
    assert 'You drop the access.key' in out
    assert 'access.key' in out
    assert 'Goodbye' in out


def test_help_then_look():
    result = subprocess.run(
        CMD,
        input='help look\nlook\nquit\n',
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert 'look: Describe the current room or a subdirectory' in out
    assert 'dimly lit terminal' in out
    assert 'Goodbye' in out
