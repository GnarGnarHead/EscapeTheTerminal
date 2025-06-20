import os
import subprocess
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(__file__))
CMD = [sys.executable, '-m', 'escape']


def test_autosave_uses_save_dir(tmp_path):
    save_dir = tmp_path / 'saves'
    save_dir.mkdir()
    env = os.environ.copy()
    env['PYTHONPATH'] = REPO_ROOT
    env['ET_AUTOSAVE'] = '1'
    env['ET_SAVE_DIR'] = str(save_dir)
    subprocess.run(
        CMD,
        input='look\nquit\n',
        text=True,
        capture_output=True,
        cwd=tmp_path,
        env=env,
    )
    assert (save_dir / 'game.sav').exists()
    assert not (tmp_path / 'game.sav').exists()


def test_load_from_save_dir(tmp_path):
    save_dir = tmp_path / 'saves'
    save_dir.mkdir()
    env = os.environ.copy()
    env['PYTHONPATH'] = REPO_ROOT
    env['ET_AUTOSAVE'] = '1'
    env['ET_SAVE_DIR'] = str(save_dir)
    subprocess.run(
        CMD,
        input='take access.key\nquit\n',
        text=True,
        capture_output=True,
        cwd=tmp_path,
        env=env,
    )
    assert (save_dir / 'game.sav').exists()

    result = subprocess.run(
        CMD,
        input='load\ninventory\nquit\n',
        text=True,
        capture_output=True,
        cwd=tmp_path,
        env=env,
    )
    assert 'Inventory: access.key' in result.stdout
