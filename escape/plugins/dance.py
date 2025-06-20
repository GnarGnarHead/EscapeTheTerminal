def dance(arg=""):
    """Print a playful dance message."""
    game._output(f"Dancing {arg}" if arg else "Dancing")

# register the command on import
if 'game' in globals():
    game.command_map['dance'] = lambda arg="": dance(arg)
