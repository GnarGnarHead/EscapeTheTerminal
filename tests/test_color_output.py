import subprocess, sys, os

SCRIPT = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'escape.py')


def test_color_env_variable():
    env = os.environ.copy()
    env['ET_COLOR'] = '1'
    result = subprocess.run(
        [sys.executable, SCRIPT],
        input='ls\nquit\n',
        text=True,
        capture_output=True,
        env=env,
    )
    out = result.stdout
    assert '\x1b[33m' in out  # directory color
    assert '\x1b[36m' in out  # item color
    assert 'Goodbye' in out


def test_color_flag():
    result = subprocess.run(
        [sys.executable, SCRIPT, '--color'],
        input='ls\nquit\n',
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert '\x1b[33m' in out
    assert '\x1b[36m' in out
    assert 'Goodbye' in out
