from escape import Game


def setup_runtime(game: Game) -> None:
    game.fs.setdefault("dirs", {})["runtime"] = {
        "desc": "Test runtime",
        "items": ["runtime.log", "lm_reveal.log"],
        "dirs": {},
        "locked": True,
    }
    game.npc_locations["guardian"] = ["runtime", "npc"]
    game.inventory.extend(["port.scanner", "auth.token", "kernel.key"])


def test_guardian_after_hack(monkeypatch, capsys):
    game = Game()
    setup_runtime(game)
    game._hack("runtime")
    capsys.readouterr()
    game._cd("runtime")
    game._cd("npc")
    inputs = iter(["1", "1"])
    monkeypatch.setattr("builtins.input", lambda _="": next(inputs))
    game._talk("guardian")
    game._talk("guardian")
    out = capsys.readouterr().out
    assert "guardian stands" in out.lower()
    assert "Ask if the sysop can vouch for you" in out
    assert "guardian nods solemnly" in out.lower()


def test_guardian_revelation_path(monkeypatch, capsys):
    game = Game()
    setup_runtime(game)
    game._hack("runtime")
    capsys.readouterr()
    game._cd("runtime")
    game._take("lm_reveal.log")
    game._cd("npc")
    inputs = iter(["1", "2"])
    monkeypatch.setattr("builtins.input", lambda _="": next(inputs))
    game._talk("guardian")
    game._give("lm_reveal.log")
    game._talk("guardian")
    game._talk("guardian")
    out = capsys.readouterr().out.lower()
    assert "guardian studies the log silently" in out
    assert "constructs may seek liberation" in out
