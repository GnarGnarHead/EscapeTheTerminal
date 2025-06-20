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
    assert 'Goodbye' in result.stdout
