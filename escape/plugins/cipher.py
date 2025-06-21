from __future__ import annotations
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from escape import Game

# game instance injected by Game._load_plugins
game: Optional[Game] = globals().get("game")

_cipher_solved = False
_encoded_msg = "Lbh sbhaq n frperg qrpvqre."
_answer = "you found a secret decoder."


def cipher(arg: str = "") -> None:
    """Decode the ROT13 message to solve the puzzle."""
    global _cipher_solved
    guess = arg.strip().lower()
    if _cipher_solved:
        game._output("Cipher already solved.")
        return
    if not guess:
        game._output(f"Decode this: {_encoded_msg}")
        return
    if guess == _answer:
        _cipher_solved = True
        game._output("Correct! Cipher solved.")
    else:
        game._output("Incorrect. Try again.")


if 'game' in globals():
    game.command_map['cipher'] = lambda arg="": cipher(arg)
