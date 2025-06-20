import subprocess, sys, os

REPO_ROOT = os.path.dirname(os.path.dirname(__file__))
CMD = [sys.executable, '-m', 'escape']


def test_color_env_variable():
    env = os.environ.copy()
    env['ET_COLOR'] = '1'
    result = subprocess.run(
        CMD,
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
        CMD + ['--color'],
        input='ls\nquit\n',
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert '\x1b[33m' in out
    assert '\x1b[36m' in out
    assert 'Goodbye' in out


def test_color_command_on_off():
    result = subprocess.run(
        CMD,
        input='color on\nls\ncolor off\nls\nquit\n',
        text=True,
        capture_output=True,
    )
    lines = result.stdout.splitlines()
    idx1 = next(i for i, line in enumerate(lines) if 'Color enabled.' in line)
    first_ls = lines[idx1 + 1]
    idx2 = next(i for i, line in enumerate(lines) if 'Color disabled.' in line)
    second_ls = lines[idx2 + 1]
    assert '\x1b[33m' in first_ls
    assert '\x1b[36m' in first_ls
    assert '\x1b[33m' not in second_ls
    assert '\x1b[36m' not in second_ls
    assert 'Goodbye' in lines[-1]


def test_color_command_toggle():
    result = subprocess.run(
        CMD,
        input='color toggle\nls\ncolor toggle\nls\nquit\n',
        text=True,
        capture_output=True,
    )
    lines = result.stdout.splitlines()
    idx1 = next(i for i, line in enumerate(lines) if 'Color enabled.' in line)
    first_ls = lines[idx1 + 1]
    idx2 = next(i for i, line in enumerate(lines) if 'Color disabled.' in line)
    second_ls = lines[idx2 + 1]
    assert '\x1b[33m' in first_ls
    assert '\x1b[33m' not in second_ls
    assert 'Goodbye' in lines[-1]


def test_custom_color_codes_env():
    env = os.environ.copy()
    env['ET_COLOR'] = '1'
    env['ET_COLOR_ITEM'] = '35'
    env['ET_COLOR_DIR'] = '32'
    result = subprocess.run(
        CMD,
        input='ls\nquit\n',
        text=True,
        capture_output=True,
        env=env,
    )
    out = result.stdout
    assert '\x1b[35m' in out
    assert '\x1b[32m' in out
    assert '\x1b[36m' not in out
    assert '\x1b[33m' not in out
    assert 'Goodbye' in out

def test_theme_command_changes_colors():
    env = os.environ.copy()
    env['ET_COLOR'] = '1'
    result = subprocess.run(
        CMD,
        input='ls\ntheme dark\nls\nquit\n',
        text=True,
        capture_output=True,
        env=env,
    )
    lines = result.stdout.splitlines()
    idx = lines.index('> Theme set to dark.')
    first_ls = lines[idx - 1]
    second_ls = lines[idx + 1]
    assert '\x1b[33m' in first_ls
    assert '\x1b[36m' in first_ls
    assert '\x1b[34m' in second_ls
    assert '\x1b[35m' in second_ls
    assert 'Goodbye' in lines[-1]


def test_theme_overrides_env_colors():
    env = os.environ.copy()
    env['ET_COLOR'] = '1'
    env['ET_COLOR_DIR'] = '32'
    env['ET_COLOR_ITEM'] = '35'
    result = subprocess.run(
        CMD,
        input='ls\ntheme neon\nls\nquit\n',
        text=True,
        capture_output=True,
        env=env,
    )
    lines = result.stdout.splitlines()
    idx = lines.index('> Theme set to neon.')
    first_ls = lines[idx - 1]
    second_ls = lines[idx + 1]
    assert '\x1b[32m' in first_ls
    assert '\x1b[35m' in first_ls
    assert '\x1b[92m' in second_ls
    assert '\x1b[95m' in second_ls
    assert '\x1b[32m' not in second_ls
    assert 'Goodbye' in lines[-1]


def test_theme_command_respects_color_toggle():
    result = subprocess.run(
        CMD,
        input='theme neon\nls\ncolor on\nls\nquit\n',
        text=True,
        capture_output=True,
    )
    lines = result.stdout.splitlines()
    idx_theme = lines.index('> Theme set to neon.')
    idx_on = lines.index('> Color enabled.')
    first_ls = lines[idx_theme + 1]
    second_ls = lines[idx_on + 1]
    assert '\x1b[' not in first_ls
    assert '\x1b[92m' in second_ls
    assert '\x1b[95m' in second_ls
    assert 'Goodbye' in lines[-1]
