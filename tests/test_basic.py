import subprocess, sys


def test_quit_command():
    result = subprocess.run(
        [sys.executable, 'escape.py'],
        input='quit\n',
        text=True,
        capture_output=True,
    )
    assert 'Goodbye' in result.stdout
    assert result.returncode == 0


def test_look_command():
    result = subprocess.run(
        [sys.executable, 'escape.py'],
        input='look\nquit\n',
        text=True,
        capture_output=True,
    )
    assert 'dimly lit terminal' in result.stdout
    assert 'access.key' in result.stdout
    assert 'Goodbye' in result.stdout


def test_inventory_empty():
    result = subprocess.run(
        [sys.executable, 'escape.py'],
        input='inventory\nquit\n',
        text=True,
        capture_output=True,
    )
    assert 'Inventory is empty' in result.stdout
    assert 'Goodbye' in result.stdout


def test_take_item_and_inventory():
    result = subprocess.run(
        [sys.executable, 'escape.py'],
        input='take access.key\ninventory\nquit\n',
        text=True,
        capture_output=True,
    )
    assert 'pick up the access.key' in result.stdout
    assert 'Inventory: access.key' in result.stdout
    assert 'Goodbye' in result.stdout
