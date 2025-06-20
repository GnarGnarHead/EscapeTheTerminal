import os
import subprocess
import sys
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
    out = result.stdout
    assert 'SYSTEM BOOT COMPLETE' in out
    assert 'Goodbye' in out

