import subprocess
import sys
import os

REPO_ROOT = os.path.dirname(os.path.dirname(__file__))
CMD = [sys.executable, '-m', 'escape']


def test_sandbox_directory_and_files():
    result = subprocess.run(
        CMD,
        input='ls\ncd sandbox\nls\ncd npc\nls\nquit\n',
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert 'sandbox/' in out
    assert 'test.script' in out
    assert 'npc/' in out
    assert 'Goodbye' in out
