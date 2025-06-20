import subprocess
import sys
import importlib.metadata


def test_console_script_invocation():
    # Ensure the console entry point is registered
    eps = importlib.metadata.entry_points()
    names = [ep.name for ep in eps.select(group='console_scripts')]
    assert 'escape-terminal' in names

    result = subprocess.run(
        [sys.executable, '-m', 'escape'],
        input='quit\n',
        text=True,
        capture_output=True,
    )
    assert 'Goodbye' in result.stdout
    assert result.returncode == 0
