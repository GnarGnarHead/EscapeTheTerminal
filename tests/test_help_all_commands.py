import pytest
from escape import Game


def test_help_for_each_command(capsys):
    game = Game()
    for cmd, desc in game.command_descriptions.items():
        game._print_help(cmd)
        out = capsys.readouterr().out
        assert f"{cmd}: {desc}" in out
