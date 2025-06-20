import os
import subprocess
import sys

SCRIPT = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'escape.py')


def test_extra_dirs_with_seed():
    env = os.environ.copy()
    env['ET_EXTRA_SEED'] = '123'
    result = subprocess.run(
        [sys.executable, SCRIPT],
        input='cd dream\nls\ncd neon_hall_0\nls\nquit\n',
        text=True,
        capture_output=True,
        env=env,
    )
    out = result.stdout
    assert 'neon_hall_0/' in out
    assert 'echoing_alcove_1/' in out
    assert 'dream0.shard' in out
    assert 'Goodbye' in out
