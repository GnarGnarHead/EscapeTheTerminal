
from __future__ import annotations

from .game import Game


def main(argv: list[str] | None = None):
    import argparse

    parser = argparse.ArgumentParser(description="Escape the Terminal")
    parser.add_argument("--color", action="store_true", help="enable ANSI colors")
    parser.add_argument("--world", metavar="file", help="path to custom world JSON")
    parser.add_argument("--prompt", metavar="text", help="custom input prompt")
    parser.add_argument(
        "--autosave",
        action="store_true",
        help="autosave after each command",
    )
    parser.add_argument(
        "--seed",
        metavar="num",
        help="seed for procedural extras",
    )
    parser.add_argument(
        "--extra-count",
        metavar="num",
        help="number of extra directories per base",
    )
    args = parser.parse_args(argv)

    import os

    if args.autosave:
        os.environ["ET_AUTOSAVE"] = "1"
    if args.seed is not None:
        os.environ["ET_EXTRA_SEED"] = str(args.seed)
    if args.extra_count is not None:
        os.environ["ET_EXTRA_COUNT"] = str(args.extra_count)

    game_color = True if args.color else None
    Game(use_color=game_color, world_file=args.world, prompt=args.prompt).run()

