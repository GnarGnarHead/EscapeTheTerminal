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


def test_hack_requires_scanner():
    result = subprocess.run(
        [sys.executable, SCRIPT],
        input='scan network\nhack network\nquit\n',
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert 'You need the port.scanner to hack this node.' in out
    assert 'Goodbye' in out


def test_cat_node_log_after_hack():
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
            'cat node.log\n'
            'quit\n'
        ),
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert 'Intrusion attempts detected.' in out
    assert 'Goodbye' in out


def test_scan_nested_node():
    result = subprocess.run(
        [sys.executable, SCRIPT],
        input=(
            'cd lab\n'
            'take port.scanner\n'
            'cd ..\n'
            'scan network\n'
            'hack network\n'
            'cd network\n'
            'scan node\n'
            'cd node\n'
            'ls\n'
            'quit\n'
        ),
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert 'Discovered node2' in out
    assert 'node2/' in out


def test_hack_node2_requires_token():
    result = subprocess.run(
        [sys.executable, SCRIPT],
        input=(
            'cd lab\n'
            'take port.scanner\n'
            'cd ..\n'
            'scan network\n'
            'hack network\n'
            'cd network\n'
            'scan node\n'
            'cd node\n'
            'hack node2\n'
            'quit\n'
        ),
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert 'You need the auth.token to hack this node.' in out


def test_hack_node2_success():
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
            'take auth.token\n'
            'cd ..\n'
            'scan node\n'
            'cd node\n'
            'hack node2\n'
            'cd node2\n'
            'ls\n'
            'quit\n'
        ),
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert 'Access granted' in out
    assert 'deep.node.log' in out
