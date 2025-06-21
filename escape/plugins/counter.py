from __future__ import annotations
from typing import TYPE_CHECKING, Optional


if TYPE_CHECKING:
    from escape import Game

game: Optional[Game] = globals().get("game")


counter_value = 0


def counter(arg=""):
    """Increment and display a counter value."""
    global counter_value
    counter_value += 1
    game._output(f"Counter: {counter_value}")


if 'game' in globals():
    game.command_map['counter'] = lambda arg="": counter(arg)
