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
