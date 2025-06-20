import os
import subprocess
import sys

CMD = [sys.executable, '-m', 'escape']


def test_prompt_env_variable():
    env = os.environ.copy()
    env['ET_PROMPT'] = '>>> '
    result = subprocess.run(
        CMD,
        input='quit\n',
        text=True,
        capture_output=True,
        env=env,
    )
    assert '>>> Goodbye' in result.stdout
