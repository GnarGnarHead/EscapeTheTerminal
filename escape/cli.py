from .game import Game


def main(argv: list[str] | None = None):
    import argparse

    parser = argparse.ArgumentParser(description="Escape the Terminal")
    parser.add_argument("--color", action="store_true", help="enable ANSI colors")
    args = parser.parse_args(argv)

    game_color = True if args.color else None
    Game(use_color=game_color).run()

