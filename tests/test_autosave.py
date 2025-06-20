import os
import subprocess
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(__file__))
CMD = [sys.executable, '-m', 'escape']


def test_autosave_creates_file(tmp_path):
    env = os.environ.copy()
    env['PYTHONPATH'] = REPO_ROOT
    env['ET_AUTOSAVE'] = '1'
    subprocess.run(
        CMD,
        input='look\nquit\n',
        text=True,
        capture_output=True,
        cwd=tmp_path,
        env=env,
    )
    assert (tmp_path / 'game.sav').exists()


def test_autosave_saves_state(tmp_path):
    env = os.environ.copy()
    env['PYTHONPATH'] = REPO_ROOT
    env['ET_AUTOSAVE'] = '1'
    subprocess.run(
        CMD,
        input='take access.key\nquit\n',
        text=True,
        capture_output=True,
        cwd=tmp_path,
        env=env,
    )
    assert (tmp_path / 'game.sav').exists()

    result = subprocess.run(
        CMD,
        input='load\ninventory\nquit\n',
        text=True,
        capture_output=True,
        cwd=tmp_path,
        env=env,
    )
    assert 'Inventory: access.key' in result.stdout

