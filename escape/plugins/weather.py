from __future__ import annotations
from typing import TYPE_CHECKING, Optional
import random

if TYPE_CHECKING:
    from escape import Game

game: Optional[Game] = globals().get("game")

weather_messages = [
    "Clear skies all around.",
    "A gentle rain begins to fall.",
    "Thunder rumbles in the distance.",
    "A dense fog settles over the area.",
]


def weather(arg: str = "") -> None:
    """Print a random weather description."""
    msg = random.choice(weather_messages)
    game._output(msg)


if 'game' in globals():
    game.command_map['weather'] = lambda arg="": weather(arg)
