from escape import Game


def setup_runtime(game: Game) -> None:
    game.fs.setdefault("dirs", {})["runtime"] = {
        "desc": "Test runtime",
        "items": ["runtime.log", "lm_reveal.log"],
        "dirs": {},
        "locked": True,
    }
    game.inventory.extend(["port.scanner", "auth.token", "kernel.key"])


def test_decode_adds_runtime_quest():
    game = Game()
    game.inventory.extend(["decoder", "mem.fragment"])
    game._decode("mem.fragment")
    assert game.quests == ["Recover your lost memory", "Trace your runtime origin."]


def test_hack_runtime_updates_quests(capsys):
    game = Game()
    game.inventory.extend(["decoder", "mem.fragment"])
    game._decode("mem.fragment")
    setup_runtime(game)
    game._hack("runtime")
    capsys.readouterr()
    assert "Trace your runtime origin." not in game.quests
    assert "Decide your fate" in game.quests

