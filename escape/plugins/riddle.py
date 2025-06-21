from __future__ import annotations
from typing import TYPE_CHECKING, Optional


if TYPE_CHECKING:
    from escape import Game

game: Optional[Game] = globals().get("game")


riddle_shown = False
_riddle = "What has to be broken before you can use it?"
_answer = "egg"


def riddle(arg: str = "") -> None:
    """A simple riddle challenge."""
    global riddle_shown
    guess = arg.strip().lower()
    if not riddle_shown:
        riddle_shown = True
        game._output(_riddle)
        return
    if not guess:
        game._output("Provide your answer.")
        return
    if guess == _answer:
        game._output("Correct! The riddle is solved.")
    else:
        game._output("Nope, try again.")


if 'game' in globals():
    game.command_map['riddle'] = lambda arg="": riddle(arg)
