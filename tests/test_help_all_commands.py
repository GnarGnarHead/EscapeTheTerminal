import pytest
from pathlib import Path

from escape import Game


def test_help_lists_all_commands(capsys):
    game = Game()
    man_dir = Path(game.data_dir) / "man"
    game._print_help()
    out = capsys.readouterr().out
    lines = [line.strip() for line in out.splitlines() if line.strip()]
    assert lines[0] == "Available commands:"
    listed_cmds = [line.split(":", 1)[0] for line in lines[1:]]
    assert listed_cmds == sorted(listed_cmds)
    for cmd, desc in game.command_descriptions.items():
        assert f"{cmd}: {desc}" in out
        assert (man_dir / f"{cmd}.man").exists()
