import os
import subprocess
import sys

CMD = [sys.executable, '-m', 'escape']

DECODE_SEQUENCE = (
    'take access.key\n'
    'use access.key\n'
    'cd hidden\n'
    'take mem.fragment\n'
    'cd ..\n'
    'cd lab\n'
    'take decoder\n'
    'decode mem.fragment\n'
    'cd ..\n'
)


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
        input=(
            DECODE_SEQUENCE +
            'cd dream\nls\nquit\n'
        ),
        text=True,
        capture_output=True,
    )
    assert 'neon_hall_0/' in result.stdout


def test_extra_count_flag():
    result = subprocess.run(
        CMD + ['--seed', '123', '--extra-count', '2'],
        input=(
            DECODE_SEQUENCE +
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


def test_version_flag():
    import importlib.metadata

    version = importlib.metadata.version('escape-the-terminal')
    result = subprocess.run(
        CMD + ['--version'],
        text=True,
        capture_output=True,
    )
    assert version in result.stdout
