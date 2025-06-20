import os
import subprocess
import sys

CMD = [sys.executable, '-m', 'escape']


def test_prompt_flag():
    result = subprocess.run(
        CMD + ['--prompt', '>>> '],
        input='quit\n',
        text=True,
        capture_output=True,
    )
    assert '>>> Goodbye' in result.stdout


def test_autosave_flag(tmp_path):
    env = os.environ.copy()
    env['PYTHONPATH'] = os.path.dirname(os.path.dirname(__file__))
    subprocess.run(
        CMD + ['--autosave'],
        input='look\nquit\n',
        text=True,
        capture_output=True,
        cwd=tmp_path,
        env=env,
    )
    assert (tmp_path / 'game.sav').exists()


def test_seed_flag():
    result = subprocess.run(
        CMD + ['--seed', '123'],
        input='cd dream\nls\nquit\n',
        text=True,
        capture_output=True,
    )
    assert 'neon_hall_0/' in result.stdout
