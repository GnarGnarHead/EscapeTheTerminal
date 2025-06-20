import pytest
from pathlib import Path

from escape import Game


def test_help_for_each_command(capsys):
    game = Game()
    man_dir = Path(game.data_dir) / "man"
    for cmd, desc in game.command_descriptions.items():
        game._print_help(cmd)
        out = capsys.readouterr().out
        assert f"{cmd}: {desc}" in out
        assert (man_dir / f"{cmd}.man").exists()
