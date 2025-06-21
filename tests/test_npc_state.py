import subprocess
import sys
import os

REPO_ROOT = os.path.dirname(os.path.dirname(__file__))
CMD = [sys.executable, "-m", "escape"]


def test_daemon_follow_up():
    result = subprocess.run(
        CMD,
        input="cd core\ncd npc\ntalk daemon\n1\n1\ntalk daemon\n1\nquit\n",
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert "acknowledges your presence" in out
    assert "sysop can help" in out
    assert "flickers, recognizing you from before" in out
    assert "I already mentioned decoding the fragment" in out
    assert "Goodbye" in out


def test_dreamer_follow_up():
    result = subprocess.run(
        CMD,
        input="cd dream\ncd npc\ntalk dreamer\n1\n2\ntalk dreamer\n1\nquit\n",
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert "dreamer watches you closely" in out
    assert "sage's wisdom" in out
    assert "nods knowingly this time" in out
    assert "Trust the path the fragment reveals" in out
    assert "Goodbye" in out


def test_sysop_polite_branch():
    result = subprocess.run(
        CMD,
        input="cd core\ncd npc\ntalk sysop\n1\ntalk sysop\n1\nquit\n",
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert "sysop glances over" in out
    assert "nods at your respect" in out
    assert "Ask about the daemon" in out
    assert "welcomes your return" in out
    assert "glitch" in out
    assert "Goodbye" in out


def test_wanderer_helped_branch():
    result = subprocess.run(
        CMD,
        input="cd dream\ncd npc\ntalk wanderer\n2\ntalk wanderer\n1\nquit\n",
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert "weary wanderer drifts" in out
    assert "Ask about the oracle" in out
    assert "shares a secret path" in out
    assert "Paths shift with each reboot" in out
    assert "Goodbye" in out


def test_sysop_rude_branch():
    result = subprocess.run(
        CMD,
        input="cd core\ncd npc\ntalk sysop\n2\ntalk sysop\n1\nquit\n",
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert "sysop glances over" in out
    assert "scowls at your tone" in out
    assert "Ask about the daemon" in out
    assert "folds their arms warily" in out
    assert "glitch" in out
    assert "Goodbye" in out


def test_wanderer_ignored_branch():
    result = subprocess.run(
        CMD,
        input="cd dream\ncd npc\ntalk wanderer\n1\ntalk wanderer\n1\nquit\n",
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert "weary wanderer drifts" in out
    assert "Ask about the oracle" in out
    assert "barely notices you" in out
    assert "Paths shift with each reboot" in out
    assert "Goodbye" in out


def test_oracle_follow_up():
    result = subprocess.run(
        CMD,
        input="cd dream\ncd oracle\ntalk oracle\n1\ntalk oracle\n1\nquit\n",
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert "oracle hovers in a loop" in out
    assert "watches your every move" in out
    assert "Ask about the wanderer" in out
    assert "Decode the echoes of your past" in out
    assert "Goodbye" in out


def test_oracle_vision_stage():
    result = subprocess.run(
        CMD,
        input="cd dream\ncd oracle\ntalk oracle\n1\ntalk oracle\n1\ntalk oracle\n1\nquit\n",
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert "oracle hovers in a loop" in out
    assert "watches your every move" in out
    assert "Ask about the wanderer" in out
    assert "unveils a vision of hidden paths" in out
    assert "images swirl before dissolving into noise" in out
    assert "Goodbye" in out


def test_archivist_progression():
    result = subprocess.run(
        CMD,
        input="cd memory\ncd npc\ntalk archivist\n1\ntalk archivist\n1\ntalk archivist\n1\ntalk archivist\nquit\n",
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert "archivist catalogues" in out
    assert "training with the mentor" in out
    assert "opens a secure drawer" in out
    assert "hands you a faded index code" in out
    assert "files away another memory" in out
    assert "Goodbye" in out


def test_archivist_after_decoding():
    result = subprocess.run(
        CMD,
        input=(
            "take access.key\n"
            "use access.key\n"
            "cd hidden\n"
            "take mem.fragment\n"
            "cd ..\n"
            "cd lab\n"
            "take decoder\n"
            "decode mem.fragment\n"
            "cd ..\n"
            "cd memory\n"
            "cd npc\n"
            "talk archivist\n"
            "1\n"
            "quit\n"
        ),
        text=True,
        capture_output=True,
    )
    out = result.stdout
    assert "nods at your decrypted fragment" in out
    assert "training with the mentor" in out
    assert "Goodbye" in out
