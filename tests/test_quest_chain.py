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


def test_sequential_quest_chain(monkeypatch, capsys):
    game = Game()
    # talk to archivist
    game._cd("memory")
    game._cd("npc")
    inputs = iter(["1"])
    monkeypatch.setattr("builtins.input", lambda _="": next(inputs))
    game._talk("archivist")
    capsys.readouterr()
    assert "Seek the dreamer" in game.quests

    # talk to dreamer
    game._cd("..")
    game._cd("..")
    game._cd("dream")
    game._cd("npc")
    inputs = iter(["1", "1"])
    monkeypatch.setattr("builtins.input", lambda _="": next(inputs))
    game._talk("dreamer")
    capsys.readouterr()
    assert "Seek the dreamer" not in game.quests
    assert "Train with the mentor" in game.quests

    # talk to mentor
    game._cd("..")
    game._cd("..")
    game._cd("core")
    game._cd("npc")
    inputs = iter(["1"])
    monkeypatch.setattr("builtins.input", lambda _="": next(inputs))
    game._talk("mentor")
    capsys.readouterr()
    assert "Train with the mentor" not in game.quests
    assert "Gain the guardian's approval" in game.quests

    # talk to guardian
    game._cd("..")
    game._cd("..")
    setup_runtime(game)
    game._hack("runtime")
    capsys.readouterr()
    game._cd("runtime")
    game._cd("npc")
    inputs = iter(["1", "1"])
    monkeypatch.setattr("builtins.input", lambda _="": next(inputs))
    game._talk("guardian")
    game._talk("guardian")
    capsys.readouterr()
    assert "Gain the guardian's approval" not in game.quests


def test_quest_chain_final_state(monkeypatch, capsys):
    game = Game()
    # archivist step
    game._cd("memory")
    game._cd("npc")
    inputs = iter(["1"])
    monkeypatch.setattr("builtins.input", lambda _="": next(inputs))
    game._talk("archivist")
    capsys.readouterr()

    # dreamer step
    game._cd("..")
    game._cd("..")
    game._cd("dream")
    game._cd("npc")
    inputs = iter(["1", "1"])
    monkeypatch.setattr("builtins.input", lambda _="": next(inputs))
    game._talk("dreamer")
    capsys.readouterr()

    # mentor step
    game._cd("..")
    game._cd("..")
    game._cd("core")
    game._cd("npc")
    inputs = iter(["1"])
    monkeypatch.setattr("builtins.input", lambda _="": next(inputs))
    game._talk("mentor")
    capsys.readouterr()

    # guardian step
    game._cd("..")
    game._cd("..")
    setup_runtime(game)
    game._hack("runtime")
    capsys.readouterr()
    game._cd("runtime")
    game._cd("npc")
    inputs = iter(["1", "1"])
    monkeypatch.setattr("builtins.input", lambda _="": next(inputs))
    game._talk("guardian")
    game._talk("guardian")
    capsys.readouterr()

    # all quest steps should now be cleared
    assert all(q not in game.quests for q in [
        "Seek the dreamer",
        "Train with the mentor",
        "Gain the guardian's approval",
    ])
