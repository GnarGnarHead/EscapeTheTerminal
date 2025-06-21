import subprocess
import sys
import os

REPO_ROOT = os.path.dirname(os.path.dirname(__file__))
CMD = [sys.executable, '-m', 'escape']


def test_sandboxer_first_and_second_stage():
    result = subprocess.run(
        CMD,
        input='cd sandbox\ncd npc\ntalk sandboxer\n1\ntalk sandboxer\n1\nquit\n',
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert 'sandboxer nods' in out
    assert '1. Ask about this place' in out
    assert 'Ask about the glitcher' in out
    assert 'Test freely' in out
    assert 'sandboxer adjusts' in out
    assert 'test.script' in out
    assert 'Goodbye' in out
