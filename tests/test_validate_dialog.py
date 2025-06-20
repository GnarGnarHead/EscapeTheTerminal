import os
import subprocess
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(__file__))


def test_validate_dialog(tmp_path):
    good = tmp_path / "good.dialog"
    good.write_text("Hello\n> Continue [glitched]\n?glitched: done\n")

    bad = tmp_path / "bad.dialog"
    bad.write_text("Oops\n> Broken [flag\n?missing colon\n")

    env = os.environ.copy()
    env["PYTHONPATH"] = REPO_ROOT

    ok = subprocess.run(
        [sys.executable, "-m", "escape.utils.validate_dialog", str(good)],
        text=True,
        capture_output=True,
        cwd=tmp_path,
        env=env,
    )
    assert ok.returncode == 0

    err = subprocess.run(
        [sys.executable, "-m", "escape.utils.validate_dialog", str(bad)],
        text=True,
        capture_output=True,
        cwd=tmp_path,
        env=env,
    )
    assert err.returncode == 1
    assert "choice missing closing ']'" in err.stderr
    assert "conditional missing ':'" in err.stderr
