import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, REPO_ROOT)

from escape import Game


def setup_runtime(game: Game) -> None:
    game.fs.setdefault("dirs", {})["runtime"] = {
        "desc": "Test runtime",
        "items": ["runtime.log", "lm_reveal.log"],
        "dirs": {},
        "locked": True,
    }
    game.inventory.extend(["port.scanner", "auth.token", "kernel.key"])


def test_hack_runtime_creates_loop_code(capsys):
    game = Game()
    setup_runtime(game)
    game._hack("runtime")
    capsys.readouterr()
    runtime = game.fs["dirs"]["runtime"]
    assert "loop.code" in runtime["items"]
    assert (game.data_dir / "loop.code").exists()


def test_runtime_log_includes_env_and_history(monkeypatch, capsys):
    monkeypatch.setenv("ET_COLOR", "1")
    game = Game()
    setup_runtime(game)
    game.command_history.extend(["look", "inventory"])
    game._hack("runtime")
    capsys.readouterr()
    game._cat("runtime.log")
    out = capsys.readouterr().out
    assert "look" in out and "inventory" in out
    assert "ET_COLOR=1" in out


def test_use_loop_code_restarts_game(capsys):
    game = Game()
    setup_runtime(game)
    game._hack("runtime")
    capsys.readouterr()
    game._cd("runtime")
    game._take("loop.code")
    capsys.readouterr()
    game._use("loop.code")
    out = capsys.readouterr().out
    assert "Loop" in out
    assert "Game restarted." in out
    assert "loop.code" not in game.inventory
