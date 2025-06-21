import subprocess
import sys
import os

REPO_ROOT = os.path.dirname(os.path.dirname(__file__))
CMD = [sys.executable, '-m', 'escape']


def test_technomancer_dialog():
    result = subprocess.run(
        CMD,
        input='cd dream\ncd tech_lab\ntalk technomancer\n1\ntalk technomancer\n1\nquit\n',
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert 'technomancer calibrates' in out
    assert '1. Inquire about glitches' in out
    assert 'Layer glitches to breach deeper security' in out
    assert 'Combine timing loops with glitch' in out
    assert 'Goodbye' in out
