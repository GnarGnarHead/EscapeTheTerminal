from __future__ import annotations

import json
import os
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover - for type hints
    from .game import Game


def generate_extra_dirs(game: "Game", bases: list[str] | str = "dream") -> None:
    """Populate directories under each base path with random subdirectories."""
    import random

    if isinstance(bases, str):
        bases = [bases]

    seed_val = os.getenv("ET_EXTRA_SEED")
    rnd = random.Random(int(seed_val)) if seed_val is not None else random.Random()
    count_val = os.getenv("ET_EXTRA_COUNT")
    try:
        fixed_count = int(count_val) if count_val is not None else None
    except ValueError:
        fixed_count = None

    adjectives = ["misty", "vivid", "neon", "echoing"]
    nouns = ["hall", "nexus", "alcove", "node"]
    item_defs = [
        ("dream.shard", "A sliver of surreal memory."),
        ("echo.bit", "An echo of a forgotten idea."),
        ("vision.chip", "A chip flickering with ephemeral scenes."),
    ]
    for base in bases:
        base_node = game.fs["dirs"].get(base)
        if not base_node:
            continue

        count = fixed_count if fixed_count is not None else rnd.randint(2, 3)
        for idx in range(count):
            dname = f"{rnd.choice(adjectives)}_{rnd.choice(nouns)}_{idx}"
            desc = f"A {rnd.choice(['strange', 'fleeting', 'curious'])} place within the dream."
            items: list[str] = []
            if rnd.random() < 0.5:
                it_name, it_desc = rnd.choice(item_defs)
                it_name = it_name.replace(".", f"{idx}.")
                items.append(it_name)
                game.item_descriptions[it_name] = it_desc
            base_node["dirs"][dname] = {"desc": desc, "items": items, "dirs": {}}


def generate_logs(game: "Game") -> None:
    """Create the logs directory with random log files."""
    import random

    game.logs_path.mkdir(exist_ok=True)
    for old in game.logs_path.glob("*.log"):
        try:
            old.unlink()
        except OSError:
            pass
    seed_val = os.getenv("ET_EXTRA_SEED")
    rnd = random.Random(int(seed_val)) if seed_val is not None else random.Random()

    count = rnd.randint(3, 5)
    files: list[str] = []
    for i in range(count):
        fname = f"system_{rnd.randint(1000, 9999)}.log"
        files.append(fname)
        lines = [
            f"INFO iteration {i}",
            ("SYSTEM BOOT COMPLETE" if i == 0 else f"DEBUG value {rnd.randint(0, 100)}"),
        ]
        with open(game.logs_path / fname, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")

    game.fs["dirs"]["logs"] = {
        "desc": "System logs are stored here.",
        "items": files,
        "dirs": {},
    }
    for name in files:
        game.item_descriptions.setdefault(name, "A cryptic system log file.")


def current_node(game: "Game") -> dict:
    node = game.fs
    for part in game.current:
        node = node["dirs"][part]
    return node


def look(game: "Game", directory: str = "") -> None:
    node = current_node(game)
    directory = directory.strip()
    if directory:
        if directory not in node["dirs"]:
            game._output(f"No such directory: {directory}")
            return
        node = node["dirs"][directory]
    game._output(node["desc"])
    entries = [d + "/" for d in node["dirs"]] + list(node["items"])
    if entries:
        game._output("You see: " + ", ".join(entries))


def ls(game: "Game") -> None:
    node = current_node(game)
    entries = [d + "/" for d in node["dirs"]] + list(node["items"])
    if entries:
        game._output(" ".join(entries))
    else:
        game._output("Nothing here.")


def pwd(game: "Game") -> None:
    path = "/".join(game.current) if game.current else "/"
    game._output(path)


def cd(game: "Game", directory: str) -> None:
    if directory in (".", ""):
        return
    if directory == "..":
        if game.current:
            game.current.pop()
            path = "/".join(game.current) if game.current else "/"
            game.visited_dirs.add("/" + path.lstrip("/"))
        else:
            game._output("Already at root.")
        return
    node = current_node(game)
    if directory in node["dirs"]:
        sub = node["dirs"][directory]
        if sub.get("locked"):
            game._output(f"{directory} is locked.")
            return
        game.current.append(directory)
        path = "/" + "/".join(game.current)
        game.visited_dirs.add(path)
    else:
        game._output(f"No such directory: {directory}")


def map_tree(game: "Game", node: dict | None = None, prefix: str = "") -> None:
    if node is None:
        node = current_node(game)
        game._output(".")

    entries = list(node.get("dirs", {}).keys()) + list(node.get("items", []))
    for idx, name in enumerate(entries):
        is_last = idx == len(entries) - 1
        connector = "└── " if is_last else "├── "
        if name in node.get("dirs", {}):
            game._output(f"{prefix}{connector}{name}/")
            next_prefix = f"{prefix}    " if is_last else f"{prefix}│   "
            map_tree(game, node["dirs"][name], next_prefix)
        else:
            game._output(f"{prefix}{connector}{name}")


def cat(game: "Game", filename: str) -> str | None:
    """Return the contents of ``filename`` from the data directory."""
    path = game.data_dir / filename
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        game._output(f"No such file: {filename}")
    except OSError as e:
        game._output(f"Failed to read {filename}: {e}")
    return None


def grep(game: "Game", arg: str) -> None:
    """Search log files for ``pattern`` optionally limited to a single file."""
    import re

    if not arg:
        game._output("Usage: grep <pattern> [file]")
        return

    parts = arg.split(maxsplit=1)
    pattern = parts[0]
    filename = parts[1] if len(parts) > 1 else None

    regex = re.compile(pattern, re.IGNORECASE)
    if filename:
        paths = [game.logs_path / filename]
        if not paths[0].exists():
            game._output(f"No such file: {filename}")
            return
    else:
        paths = sorted(game.logs_path.glob("*.log"))

    found = False
    for path in paths:
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except OSError:
            continue
        for lineno, line in enumerate(lines, 1):
            if regex.search(line):
                game._output(f"{path.name}:{lineno}:{line}")
                found = True
    if not found:
        game._output("No matches found.")


def save(game: "Game", slot: str = "") -> None:
    fname = game.save_file if not slot else f"game{slot}.sav"
    path = game.save_dir / fname
    data = {
        "fs": game.fs,
        "inventory": game.inventory,
        "current": game.current,
        "glitch_mode": game.glitch_mode,
        "glitch_steps": game.glitch_steps,
        "npc_state": game.npc_state,
        "npc_global_flags": game.npc_global_flags,
        "npc_trust": game.npc_trust,
        "aliases": game.aliases,
        "command_history": game.command_history,
        "journal": game.journal,
        "quests": game.quests,
        "score": game.score,
        "achievements": game.achievements,
    }
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f)
    except OSError as e:
        game._output(f"Failed to save: {e}")
    else:
        game._output("Game saved.")


def load(game: "Game", slot: str = "") -> None:
    fname = game.save_file if not slot else f"game{slot}.sav"
    path = game.save_dir / fname
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        game._output("No save file found.")
        return
    except OSError as e:
        game._output(f"Failed to load: {e}")
        return
    game.fs = data.get("fs", game.fs)
    game.inventory = data.get("inventory", [])
    game.current = data.get("current", [])
    game.glitch_mode = data.get("glitch_mode", False)
    game.glitch_steps = data.get("glitch_steps", 0)
    game.npc_state = data.get("npc_state", {})
    game.npc_global_flags = data.get("npc_global_flags", {})
    game.npc_trust = data.get("npc_trust", {})
    game.aliases = data.get("aliases", {})
    game.command_history = data.get("command_history", [])
    game.journal = data.get("journal", [])
    game.quests = data.get("quests", [])
    game.score = data.get("score", 0)
    game.achievements = data.get("achievements", [])
    game._output("Game loaded.")
