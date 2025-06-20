import subprocess
import sys
import os

REPO_ROOT = os.path.dirname(os.path.dirname(__file__))
CMD = [sys.executable, '-m', 'escape']


def test_sage_first_and_second_stage():
    result = subprocess.run(
        CMD,
        input='cd archive\ncd npc\ntalk sage\n1\ntalk sage\n1\nquit\n',
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert 'sage sits quietly' in out
    assert '1. Seek wisdom' in out
    assert 'Patience reveals hidden truths.' in out
    assert 'sage smiles gently at your approach' in out
    assert 'Knowledge flows to those who listen.' in out
    assert 'Goodbye' in out

