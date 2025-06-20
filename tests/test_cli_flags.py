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


def test_extra_count_flag():
    result = subprocess.run(
        CMD + ['--seed', '123', '--extra-count', '2'],
        input=(
            'cd dream\nls\ncd ..\n'
            'cd memory\nls\ncd ..\n'
            'cd core\nls\nquit\n'
        ),
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert 'misty_alcove_0/' in out
    assert 'neon_alcove_0/' in out
    assert 'echoing_hall_1/' in out
