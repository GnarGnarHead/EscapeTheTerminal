"""Utility to validate NPC dialog files."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


def _dialog_files(arg: str) -> list[Path]:
    p = Path(arg)
    if p.is_dir():
        return list(p.glob("*.dialog"))
    return [p]


def _check_file(path: Path) -> int:
    errors = 0
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as e:
        print(f"{path}: {e}", file=sys.stderr)
        return 1

    sections = [[]]
    for line in lines:
        if line.strip() == "---":
            sections.append([])
            continue
        sections[-1].append(line)

    if not any(sections):
        print(f"{path}: file is empty", file=sys.stderr)
        errors += 1

    for s_idx, section in enumerate(sections, 1):
        for l_idx, line in enumerate(section, 1):
            stripped = line.lstrip()
            if stripped.startswith(">"):
                choice = stripped[1:].strip()
                if "[" in choice and not choice.endswith("]"):
                    print(
                        f"{path}:{s_idx}:{l_idx}: choice missing closing ']'",
                        file=sys.stderr,
                    )
                    errors += 1
            elif stripped.startswith("?"):
                if ":" not in stripped[1:]:
                    print(
                        f"{path}:{s_idx}:{l_idx}: conditional missing ':'",
                        file=sys.stderr,
                    )
                    errors += 1
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check .dialog files for common mistakes"
    )
    parser.add_argument("paths", nargs="+", help="dialog files or directories")
    args = parser.parse_args(argv)

    total = 0
    for arg in args.paths:
        for path in _dialog_files(arg):
            total += _check_file(path)

    if total:
        print(f"{total} issue(s) found.", file=sys.stderr)
    return 1 if total else 0


if __name__ == "__main__":
    raise SystemExit(main())
