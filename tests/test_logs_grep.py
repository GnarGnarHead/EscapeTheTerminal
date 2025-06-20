import os
import subprocess
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from escape import Game

SCRIPT = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'escape.py')


def test_log_files_created(tmp_path):
    game = Game()
    log_dir = game.logs_path
    assert log_dir.exists()
    files = list(log_dir.glob('*.log'))
    assert len(files) >= 3
    assert 'logs' in game.fs['dirs']
    assert set(game.fs['dirs']['logs']['items']) == {f.name for f in files}


def test_grep_finds_boot_message():
    result = subprocess.run(
        [sys.executable, SCRIPT],
        input='grep BOOT\nquit\n',
        text=True,
        capture_output=True,
    )
    out = result.stdout.splitlines()
    boot_lines = [line for line in out if 'SYSTEM BOOT COMPLETE' in line]
    assert boot_lines, 'boot message not found'
    prefix = boot_lines[0].split(':')
    assert prefix[0].endswith('.log')
    assert prefix[1].isdigit()
    assert 'SYSTEM BOOT COMPLETE' in boot_lines[0]
    assert 'Goodbye' in result.stdout


def test_grep_specific_file(tmp_path):
    env = os.environ.copy()
    env['ET_EXTRA_SEED'] = '123'
    os.environ['ET_EXTRA_SEED'] = '123'
    game = Game()
    target = sorted(game.logs_path.glob('*.log'))[0].name
    result = subprocess.run(
        [sys.executable, SCRIPT],
        input=f'grep iteration {target}\nquit\n',
        text=True,
        capture_output=True,
        env=env,
    )
    out = result.stdout
    assert f'{target}:1:' in out
    assert 'INFO iteration' in out
    assert out.count(f'{target}:') == 1
    assert 'Goodbye' in out

    os.environ.pop('ET_EXTRA_SEED', None)

