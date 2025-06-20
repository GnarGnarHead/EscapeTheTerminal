import subprocess, sys, os

SCRIPT = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'escape.py')


def test_scan_reveals_locked_node():
    result = subprocess.run(
        [sys.executable, SCRIPT],
        input='scan network\ncd network\nls\ncd node\nquit\n',
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert 'Discovered node' in out
    assert 'node/' in out
    assert 'node is locked' in out
    assert 'Goodbye' in out


def test_hack_unlocks_node():
    result = subprocess.run(
        [sys.executable, SCRIPT],
        input=(
            'cd lab\n'
            'take port.scanner\n'
            'cd ..\n'
            'scan network\n'
            'hack network\n'
            'cd network\n'
            'cd node\n'
            'ls\n'
            'quit\n'
        ),
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert 'Access granted' in out
    assert 'node.log' in out
    assert 'Goodbye' in out
