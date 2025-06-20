import subprocess, sys


def run_game(commands):
    return subprocess.run(
        [sys.executable, 'escape.py'],
        input="\n".join(commands) + "\n",
        text=True,
        capture_output=True,
    )


def test_quit_command():
    result = run_game(['quit'])
    assert 'Goodbye' in result.stdout
    assert result.returncode == 0


def test_ls_root():
    result = run_game(['ls', 'quit'])
    # root directory should list readme.txt, home, logs
    assert 'readme.txt' in result.stdout
    assert 'home' in result.stdout
    assert 'logs' in result.stdout


def test_cd_and_cat():
    result = run_game(['cd home', 'cat note.txt', 'quit'])
    assert 'The system feels old' in result.stdout
