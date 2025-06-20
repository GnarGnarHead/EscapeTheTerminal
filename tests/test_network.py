import subprocess, sys, os

REPO_ROOT = os.path.dirname(os.path.dirname(__file__))
CMD = [sys.executable, '-m', 'escape']


def test_scan_reveals_locked_node():
    result = subprocess.run(
        CMD,
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
        CMD,
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
        CMD,
        input='scan network\nhack network\nquit\n',
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert 'You need the port.scanner to hack this node.' in out
    assert 'Goodbye' in out


def test_cat_node_log_after_hack():
    result = subprocess.run(
        CMD,
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
        CMD,
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
        CMD,
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
        CMD,
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
    assert 'firmware.patch' in out


def test_scan_node3_after_hack_node2():
    result = subprocess.run(
        CMD,
        input=(
            'cd lab\n'
            'take port.scanner\n'
            'cd ..\n'
            'scan network\n'
            'hack network\n'
            'cd network\n'
            'scan node\n'
            'cd node\n'
            'take auth.token\n'
            'hack node2\n'
            'scan node2\n'
            'quit\n'
        ),
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert 'Discovered node3' in out


def test_hack_node3_requires_patch():
    result = subprocess.run(
        CMD,
        input=(
            'cd lab\n'
            'take port.scanner\n'
            'cd ..\n'
            'scan network\n'
            'hack network\n'
            'cd network\n'
            'scan node\n'
            'cd node\n'
            'take auth.token\n'
            'hack node2\n'
            'scan node2\n'
            'cd node2\n'
            'hack node3\n'
            'quit\n'
        ),
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert 'You need the firmware.patch to hack this node.' in out


def test_hack_node3_success():
    result = subprocess.run(
        CMD,
        input=(
            'cd lab\n'
            'take port.scanner\n'
            'cd ..\n'
            'scan network\n'
            'hack network\n'
            'cd network\n'
            'scan node\n'
            'cd node\n'
            'take auth.token\n'
            'hack node2\n'
            'scan node2\n'
            'cd node2\n'
            'take firmware.patch\n'
            'hack node3\n'
            'cd node3\n'
            'ls\n'
            'quit\n'
        ),
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert 'Access granted' in out
    assert 'deep.node.log' in out
