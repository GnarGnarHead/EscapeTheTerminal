
from __future__ import annotations

from .game import Game


def main(argv: list[str] | None = None):
    import argparse

    parser = argparse.ArgumentParser(description="Escape the Terminal")
    parser.add_argument("--color", action="store_true", help="enable ANSI colors")
    parser.add_argument("--world", metavar="file", help="path to custom world JSON")
    args = parser.parse_args(argv)

    game_color = True if args.color else None
    Game(use_color=game_color, world_file=args.world).run()

