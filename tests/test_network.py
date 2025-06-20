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


def test_scan_node4_after_hack_node3():
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
            'scan node3\n'
            'quit\n'
        ),
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert 'Discovered node4' in out


def test_hack_node4_requires_root_access():
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
            'scan node3\n'
            'cd node3\n'
            'hack node4\n'
            'quit\n'
        ),
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert 'You need the root.access to hack this node.' in out


def test_hack_node4_success():
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
            'scan node3\n'
            'cd node3\n'
            'take root.access\n'
            'hack node4\n'
            'cd node4\n'
            'ls\n'
            'quit\n'
        ),
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert 'Access granted' in out
    assert 'deep.node.log' in out


def test_scan_node5_after_hack_node4():
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
            'scan node3\n'
            'cd node3\n'
            'take root.access\n'
            'hack node4\n'
            'scan node4\n'
            'quit\n'
        ),
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert 'Discovered node5' in out


def test_hack_node5_requires_super_user():
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
            'scan node3\n'
            'cd node3\n'
            'take root.access\n'
            'hack node4\n'
            'scan node4\n'
            'cd node4\n'
            'hack node5\n'
            'quit\n'
        ),
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert 'You need the super.user to hack this node.' in out


def test_hack_node5_success():
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
            'scan node3\n'
            'cd node3\n'
            'take root.access\n'
            'hack node4\n'
            'scan node4\n'
            'cd node4\n'
            'take super.user\n'
            'hack node5\n'
            'cd node5\n'
            'ls\n'
            'quit\n'
        ),
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert 'Access granted' in out
    assert 'deep.node.log' in out


def test_scan_node6_after_hack_node5():
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
            'scan node3\n'
            'cd node3\n'
            'take root.access\n'
            'hack node4\n'
            'scan node4\n'
            'cd node4\n'
            'take super.user\n'
            'hack node5\n'
            'scan node5\n'
            'quit\n'
        ),
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert 'Discovered node6' in out


def test_hack_node6_requires_admin_override():
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
            'scan node3\n'
            'cd node3\n'
            'take root.access\n'
            'hack node4\n'
            'scan node4\n'
            'cd node4\n'
            'take super.user\n'
            'hack node5\n'
            'scan node5\n'
            'cd node5\n'
            'hack node6\n'
            'quit\n'
        ),
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert 'You need the admin.override to hack this node.' in out


def test_hack_node6_success():
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
            'scan node3\n'
            'cd node3\n'
            'take root.access\n'
            'hack node4\n'
            'scan node4\n'
            'cd node4\n'
            'take super.user\n'
            'hack node5\n'
            'scan node5\n'
            'cd node5\n'
            'take admin.override\n'
            'hack node6\n'
            'cd node6\n'
            'ls\n'
            'quit\n'
        ),
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert 'Access granted' in out
    assert 'kernel.key' in out


def test_scan_node7_after_hack_node6():
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
            'scan node3\n'
            'cd node3\n'
            'take root.access\n'
            'hack node4\n'
            'scan node4\n'
            'cd node4\n'
            'take super.user\n'
            'hack node5\n'
            'scan node5\n'
            'cd node5\n'
            'take admin.override\n'
            'hack node6\n'
            'scan node6\n'
            'quit\n'
        ),
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert 'Discovered node7' in out


def test_hack_node7_requires_kernel_key():
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
            'scan node3\n'
            'cd node3\n'
            'take root.access\n'
            'hack node4\n'
            'scan node4\n'
            'cd node4\n'
            'take super.user\n'
            'hack node5\n'
            'scan node5\n'
            'cd node5\n'
            'take admin.override\n'
            'hack node6\n'
            'scan node6\n'
            'cd node6\n'
            'hack node7\n'
            'quit\n'
        ),
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert 'You need the kernel.key to hack this node.' in out


def test_hack_node7_success():
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
            'scan node3\n'
            'cd node3\n'
            'take root.access\n'
            'hack node4\n'
            'scan node4\n'
            'cd node4\n'
            'take super.user\n'
            'hack node5\n'
            'scan node5\n'
            'cd node5\n'
            'take admin.override\n'
            'hack node6\n'
            'scan node6\n'
            'cd node6\n'
            'take kernel.key\n'
            'hack node7\n'
            'cd node7\n'
            'ls\n'
            'quit\n'
        ),
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert 'Access granted' in out
    assert 'master.process' in out


def test_scan_node8_after_hack_node7():
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
            'scan node3\n'
            'cd node3\n'
            'take root.access\n'
            'hack node4\n'
            'scan node4\n'
            'cd node4\n'
            'take super.user\n'
            'hack node5\n'
            'scan node5\n'
            'cd node5\n'
            'take admin.override\n'
            'hack node6\n'
            'scan node6\n'
            'cd node6\n'
            'take kernel.key\n'
            'hack node7\n'
            'scan node7\n'
            'quit\n'
        ),
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert 'Discovered node8' in out


def test_hack_node8_requires_master_process():
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
            'scan node3\n'
            'cd node3\n'
            'take root.access\n'
            'hack node4\n'
            'scan node4\n'
            'cd node4\n'
            'take super.user\n'
            'hack node5\n'
            'scan node5\n'
            'cd node5\n'
            'take admin.override\n'
            'hack node6\n'
            'scan node6\n'
            'cd node6\n'
            'take kernel.key\n'
            'hack node7\n'
            'scan node7\n'
            'cd node7\n'
            'hack node8\n'
            'quit\n'
        ),
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert 'You need the master.process to hack this node.' in out


def test_hack_node8_success():
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
            'scan node3\n'
            'cd node3\n'
            'take root.access\n'
            'hack node4\n'
            'scan node4\n'
            'cd node4\n'
            'take super.user\n'
            'hack node5\n'
            'scan node5\n'
            'cd node5\n'
            'take admin.override\n'
            'hack node6\n'
            'scan node6\n'
            'cd node6\n'
            'take kernel.key\n'
            'hack node7\n'
            'scan node7\n'
            'cd node7\n'
            'take master.process\n'
            'hack node8\n'
            'cd node8\n'
            'ls\n'
            'quit\n'
        ),
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert 'Access granted' in out
    assert 'hypervisor.command' in out


def test_scan_node9_after_hack_node8():
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
            'scan node3\n'
            'cd node3\n'
            'take root.access\n'
            'hack node4\n'
            'scan node4\n'
            'cd node4\n'
            'take super.user\n'
            'hack node5\n'
            'scan node5\n'
            'cd node5\n'
            'take admin.override\n'
            'hack node6\n'
            'scan node6\n'
            'cd node6\n'
            'take kernel.key\n'
            'hack node7\n'
            'scan node7\n'
            'cd node7\n'
            'take master.process\n'
            'hack node8\n'
            'scan node8\n'
            'quit\n'
        ),
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert 'Discovered node9' in out


def test_hack_node9_requires_hypervisor_command():
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
            'scan node3\n'
            'cd node3\n'
            'take root.access\n'
            'hack node4\n'
            'scan node4\n'
            'cd node4\n'
            'take super.user\n'
            'hack node5\n'
            'scan node5\n'
            'cd node5\n'
            'take admin.override\n'
            'hack node6\n'
            'scan node6\n'
            'cd node6\n'
            'take kernel.key\n'
            'hack node7\n'
            'scan node7\n'
            'cd node7\n'
            'take master.process\n'
            'hack node8\n'
            'scan node8\n'
            'cd node8\n'
            'hack node9\n'
            'quit\n'
        ),
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert 'You need the hypervisor.command to hack this node.' in out


def test_hack_node9_success():
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
            'scan node3\n'
            'cd node3\n'
            'take root.access\n'
            'hack node4\n'
            'scan node4\n'
            'cd node4\n'
            'take super.user\n'
            'hack node5\n'
            'scan node5\n'
            'cd node5\n'
            'take admin.override\n'
            'hack node6\n'
            'scan node6\n'
            'cd node6\n'
            'take kernel.key\n'
            'hack node7\n'
            'scan node7\n'
            'cd node7\n'
            'take master.process\n'
            'hack node8\n'
            'scan node8\n'
            'cd node8\n'
            'take hypervisor.command\n'
            'hack node9\n'
            'cd node9\n'
            'ls\n'
            'quit\n'
        ),
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert 'Access granted' in out
    assert 'quantum.access' in out


def test_scan_runtime_after_hack_node9():
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
            'scan node3\n'
            'cd node3\n'
            'take root.access\n'
            'hack node4\n'
            'scan node4\n'
            'cd node4\n'
            'take super.user\n'
            'hack node5\n'
            'scan node5\n'
            'cd node5\n'
            'take admin.override\n'
            'hack node6\n'
            'scan node6\n'
            'cd node6\n'
            'take kernel.key\n'
            'hack node7\n'
            'scan node7\n'
            'cd node7\n'
            'take master.process\n'
            'hack node8\n'
            'scan node8\n'
            'cd node8\n'
            'take hypervisor.command\n'
            'hack node9\n'
            'scan node9\n'
            'quit\n'
        ),
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert 'Discovered runtime' in out


def test_hack_runtime_requires_kernel_key():
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
            'scan node3\n'
            'cd node3\n'
            'take root.access\n'
            'hack node4\n'
            'scan node4\n'
            'cd node4\n'
            'take super.user\n'
            'hack node5\n'
            'scan node5\n'
            'cd node5\n'
            'take admin.override\n'
            'hack node6\n'
            'scan node6\n'
            'cd node6\n'
            'take kernel.key\n'
            'hack node7\n'
            'scan node7\n'
            'cd node7\n'
            'take master.process\n'
            'hack node8\n'
            'scan node8\n'
            'cd node8\n'
            'take hypervisor.command\n'
            'hack node9\n'
            'scan node9\n'
            'cd node9\n'
            'drop kernel.key\n'
            'hack runtime\n'
            'quit\n'
        ),
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert 'You need the kernel.key to hack this node.' in out


def test_hack_runtime_success():
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
            'scan node3\n'
            'cd node3\n'
            'take root.access\n'
            'hack node4\n'
            'scan node4\n'
            'cd node4\n'
            'take super.user\n'
            'hack node5\n'
            'scan node5\n'
            'cd node5\n'
            'take admin.override\n'
            'hack node6\n'
            'scan node6\n'
            'cd node6\n'
            'take kernel.key\n'
            'hack node7\n'
            'scan node7\n'
            'cd node7\n'
            'take master.process\n'
            'hack node8\n'
            'scan node8\n'
            'cd node8\n'
            'take hypervisor.command\n'
            'hack node9\n'
            'scan node9\n'
            'cd node9\n'
            'hack runtime\n'
            'cd runtime\n'
            'cat runtime.log\n'
            'quit\n'
        ),
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert 'Access granted' in out
    assert 'A log revealing your runtime environment and history.' in out
