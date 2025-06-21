import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from escape import Game

    game: Game


THEMES = {
    'dark': ("\x1b[34m", "\x1b[35m"),  # blue directories, magenta items
    'mono': ("\x1b[37m", "\x1b[37m"),  # white directories and items
    'neon': ("\x1b[92m", "\x1b[95m"),  # bright green dirs, bright magenta items
}


def _valid_code(code: str) -> bool:
    """Return True if ``code`` looks like an ANSI color number list."""
    return bool(re.fullmatch(r"\d+(;\d+)*", code))


def theme(arg: str = "") -> None:
    """Switch between predefined color themes or set custom codes."""
    text = arg.strip()
    if not text:
        game._output("Usage: theme [dark|mono|neon|<dir> <item>]")
        return

    tokens = text.split()
    name = tokens[0].lower()
    if name in THEMES and len(tokens) == 1:
        game.dir_color, game.item_color = THEMES[name]
        game._output(f"Theme set to {name}.")
        return

    if len(tokens) != 2 or not all(_valid_code(t) for t in tokens):
        game._output("Usage: theme [dark|mono|neon|<dir> <item>]")
        return

    dir_code, item_code = tokens
    game.dir_color = f"\x1b[{dir_code}m"
    game.item_color = f"\x1b[{item_code}m"
    game._output("Theme set to custom.")


if 'game' in globals():
    game.command_map['theme'] = lambda arg="": theme(arg)
