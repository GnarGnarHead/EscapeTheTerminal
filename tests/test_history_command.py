import os
import subprocess
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(__file__))
CMD = [sys.executable, '-m', 'escape']


def test_history_persists_after_save_load(tmp_path):
    env = os.environ.copy()
    env['PYTHONPATH'] = REPO_ROOT
    subprocess.run(
        CMD,
        input='look\nsave\nquit\n',
        text=True,
        capture_output=True,
        cwd=tmp_path,
        env=env,
    )

    result = subprocess.run(
        CMD,
        input='load\nhistory\nquit\n',
        text=True,
        capture_output=True,
        cwd=tmp_path,
        env=env,
    )
    out = result.stdout
    assert '> look\nsave\nhistory' in out
    assert 'Goodbye' in out
