from __future__ import annotations
from typing import TYPE_CHECKING, Optional


if TYPE_CHECKING:
    from escape import Game

game: Optional[Game] = globals().get("game")


def dance(arg=""):
    """Print a playful dance message."""
    game._output(f"Dancing {arg}" if arg else "Dancing")


# register the command on import
if 'game' in globals():
    game.command_map['dance'] = lambda arg="": dance(arg)
