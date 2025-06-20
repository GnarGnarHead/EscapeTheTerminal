puzzle_solved = False

_encoded_msg = "Uifsf jt b tfdsfu nfttbhf."
_answer = "there is a secret message."

def puzzle(arg: str = "") -> None:
    """Small code-breaking challenge."""
    global puzzle_solved
    if puzzle_solved:
        game._output("Puzzle already solved.")
        return
    guess = arg.strip().lower()
    if not guess:
        game._output(f"Decode this: {_encoded_msg}")
        return
    if guess == _answer:
        puzzle_solved = True
        game._output("Correct! Puzzle solved.")
    else:
        game._output("Incorrect. Try again.")


if 'game' in globals():
    game.command_map['puzzle'] = lambda arg="": puzzle(arg)
