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


def use_loop_code(game: Game, capsys) -> None:
    setup_runtime(game)
    game._hack("runtime")
    capsys.readouterr()
    game._cd("runtime")
    game._take("loop.code")
    capsys.readouterr()
    game._use("loop.code")
    capsys.readouterr()


def test_loop_code_unlocks_void(monkeypatch, capsys):
    game = Game()
    use_loop_code(game, capsys)
    assert "void" in game.fs["dirs"]
    assert "locked" not in game.fs["dirs"]["void"]
    assert game.npc_locations["wanderer"] == ["void", "npc"]
    game._cd("void")
    game._cd("npc")
    game._talk("wanderer")
    out = capsys.readouterr().out
    assert "void" in out
    assert "Explore the void" in game.quests
