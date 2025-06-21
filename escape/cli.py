
from __future__ import annotations

from .game import Game

import importlib.metadata


def main(argv: list[str] | None = None):
    import argparse

    parser = argparse.ArgumentParser(description="Escape the Terminal")
    parser.add_argument("--color", action="store_true", help="enable ANSI colors")
    parser.add_argument("--world", metavar="file", help="path to custom world JSON")
    parser.add_argument("--prompt", metavar="text", help="custom input prompt")
    parser.add_argument(
        "--plugin-path",
        metavar="path",
        help="additional plugin directories (separated by os.pathsep)",
    )
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
    parser.add_argument(
        "--version",
        action="store_true",
        help="show program version and exit",
    )
    args = parser.parse_args(argv)

    if args.version:
        print(importlib.metadata.version("escape-the-terminal"))
        return

    import os

    if args.autosave:
        os.environ["ET_AUTOSAVE"] = "1"
    if args.plugin_path:
        os.environ["ET_PLUGIN_PATH"] = args.plugin_path
    if args.seed is not None:
        os.environ["ET_EXTRA_SEED"] = str(args.seed)
    if args.extra_count is not None:
        os.environ["ET_EXTRA_COUNT"] = str(args.extra_count)

    game_color = True if args.color else None
    Game(use_color=game_color, world_file=args.world, prompt=args.prompt).run()
