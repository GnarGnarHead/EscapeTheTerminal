THEMES = {
    'dark': ("\x1b[34m", "\x1b[35m"),  # blue directories, magenta items
    'mono': ("\x1b[37m", "\x1b[37m"),  # white directories and items
    'neon': ("\x1b[92m", "\x1b[95m"),  # bright green dirs, bright magenta items
}


def theme(arg: str = "") -> None:
    """Switch between predefined color themes."""
    name = arg.strip().lower()
    if name not in THEMES:
        game._output("Usage: theme [dark|mono|neon]")
        return
    game.dir_color, game.item_color = THEMES[name]
    game._output(f"Theme set to {name}.")


if 'game' in globals():
    game.command_map['theme'] = lambda arg="": theme(arg)
