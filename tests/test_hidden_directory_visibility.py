import subprocess
import sys

CMD = [sys.executable, '-m', 'escape']


def test_hidden_directory_visible_after_unlock():
    result = subprocess.run(
        CMD,
        input='ls\ntake access.key\nuse access.key on door\nls\nquit\n',
        text=True,
        capture_output=True,
    )
    out = result.stdout
    # hidden directory should not appear before using the key, but should after
    assert out.count('hidden/') == 1
    assert 'Goodbye' in out
