import os
import subprocess
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(__file__))
CMD = [sys.executable, '-m', 'escape']


def test_reality_directory_and_files():
    result = subprocess.run(
        CMD,
        input='ls\ncd reality\nls\ncat mirror.log\ncat truth.log\nquit\n',
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert 'reality/' in out
    assert 'mirror.log' in out
    assert 'truth.log' in out
    assert 'fragments of your true self' in out
    assert 'unfiltered and absolute' in out
    assert 'Goodbye' in out
