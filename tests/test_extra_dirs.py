import os
import subprocess
import sys

SCRIPT = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'escape.py')


def test_extra_dirs_with_seed():
    env = os.environ.copy()
    env['ET_EXTRA_SEED'] = '123'
    result = subprocess.run(
        [sys.executable, SCRIPT],
        input=(
            'cd dream\nls\ncd neon_hall_0\nls\ncd ..\ncd ..\n'
            'cd memory\nls\ncd ..\ncd core\nls\nquit\n'
        ),
        text=True,
        capture_output=True,
        env=env,
    )
    out = result.stdout
    assert 'neon_hall_0/' in out
    assert 'echoing_alcove_1/' in out
    assert 'dream0.shard' in out
    assert 'vivid_alcove_0/' in out
    assert 'vivid_hall_1/' in out
    assert 'misty_hall_0/' in out
    assert 'vivid_hall_2/' in out
    assert 'Goodbye' in out


def test_extra_dirs_with_seed_and_count():
    env = os.environ.copy()
    env['ET_EXTRA_SEED'] = '123'
    env['ET_EXTRA_COUNT'] = '2'
    result = subprocess.run(
        [sys.executable, SCRIPT],
        input=(
            'cd dream\nls\ncd ..\n'
            'cd memory\nls\ncd ..\n'
            'cd core\nls\nquit\n'
        ),
        text=True,
        capture_output=True,
        env=env,
    )
    out = result.stdout
    assert 'misty_alcove_0/' in out
    assert 'neon_hall_1/' in out
    assert 'neon_alcove_0/' in out
    assert 'neon_nexus_1/' in out
    assert 'misty_node_0/' in out
    assert 'echoing_hall_1/' in out
    assert 'Goodbye' in out
