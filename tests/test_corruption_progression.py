import sys, os
from escape import Game


def test_corruption_messages_and_scrambling(capsys):
    game = Game()
    game.corruption = 99  # just below 25%
    game._output("hello")
    assert "CORRUPTION" not in capsys.readouterr().out

    game.corruption = 100  # crosses 25%
    msg25 = game._apply_corruption("hello")
    game._output("hello")
    out = capsys.readouterr().out
    assert "-- CORRUPTION 25% --" in out
    assert msg25 in out

    game.corruption = 200  # crosses 50%
    msg50 = game._apply_corruption("test")
    game._output("test")
    out = capsys.readouterr().out
    assert "-- CORRUPTION 50% --" in out
    assert msg50 in out

    game.corruption = 300  # crosses 75%
    msg75 = game._apply_corruption("final")
    game._output("final")
    out = capsys.readouterr().out
    assert "-- CORRUPTION 75% --" in out
    assert msg75 in out


def test_corruption_counter_increments(monkeypatch):
    game = Game()
    inputs = iter(["look", "look", "quit"])
    monkeypatch.setattr('builtins.input', lambda _='': next(inputs))
    game.run()
    assert game.corruption == 3
