import subprocess
import sys
import os

REPO_ROOT = os.path.dirname(os.path.dirname(__file__))
CMD = [sys.executable, '-m', 'escape']


def test_mentor_first_and_second_stage():
    result = subprocess.run(
        CMD,
        input='cd core\ncd npc\ntalk mentor\n1\ntalk mentor\n1\nquit\n',
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert 'mentor studies you' in out
    assert '1. Request training' in out
    assert 'Focus is the foundation of mastery.' in out
    assert 'mentor nods approvingly' in out
    assert 'Practice turns knowledge into skill.' in out
    assert 'Goodbye' in out
