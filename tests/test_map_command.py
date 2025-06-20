import os
import subprocess
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(__file__))
CMD = [sys.executable, '-m', 'escape']


def test_map_root():
    env = os.environ.copy()
    env['ET_EXTRA_SEED'] = '123'
    env['PYTHONPATH'] = REPO_ROOT
    result = subprocess.run(
        CMD,
        input='map\nquit\n',
        text=True,
        capture_output=True,
        env=env,
    )
    out = result.stdout
    assert '.' in out
    assert 'lab/' in out
    assert 'archive/' in out
    assert 'dream/' in out
    assert 'memory/' in out
    assert 'Goodbye' in out


def test_map_after_unlock_hidden():
    env = os.environ.copy()
    env['ET_EXTRA_SEED'] = '123'
    env['PYTHONPATH'] = REPO_ROOT
    result = subprocess.run(
        CMD,
        input='take access.key\nuse access.key\nmap\nquit\n',
        text=True,
        capture_output=True,
        env=env,
    )
    out = result.stdout
    assert 'hidden/' in out
    assert 'vault/' in out
    assert 'mem.fragment' in out
    assert 'treasure.txt' in out
    assert 'Goodbye' in out


def test_map_inside_subdir():
    env = os.environ.copy()
    env['ET_EXTRA_SEED'] = '123'
    env['PYTHONPATH'] = REPO_ROOT
    result = subprocess.run(
        CMD,
        input='cd dream\ncd subconscious\nmap\nquit\n',
        text=True,
        capture_output=True,
        env=env,
    )
    out = result.stdout
    assert '.\n' in out
    assert 'reverie.log' in out
    assert 'Goodbye' in out

