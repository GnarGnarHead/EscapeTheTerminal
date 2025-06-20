import subprocess
import sys


def test_console_script_invocation():
    # Install the project in editable mode
    subprocess.run(
        [sys.executable, '-m', 'pip', 'install', '-e', '.', '--no-deps', '--quiet'],
        check=True,
    )
    result = subprocess.run(
        ['escape-terminal'],
        input='quit\n',
        text=True,
        capture_output=True,
    )
    assert 'Goodbye' in result.stdout
    assert result.returncode == 0
