from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from .game import Game


def update_quests_after_talk(game: "Game", npc: str) -> None:
    """Modify quest list based on conversation progression."""
    if npc == "archivist" and game.npc_global_flags.get("archivist_met"):
        if "Seek the dreamer" not in game.quests:
            game.quests.append("Seek the dreamer")
    elif npc == "dreamer" and game.npc_global_flags.get("dreamer_met"):
        if "Seek the dreamer" in game.quests:
            game.quests.remove("Seek the dreamer")
        if "Train with the mentor" not in game.quests:
            game.quests.append("Train with the mentor")
    elif npc == "mentor" and game.npc_global_flags.get("mentor_met"):
        if "Train with the mentor" in game.quests:
            game.quests.remove("Train with the mentor")
        if "Gain the guardian's approval" not in game.quests:
            game.quests.append("Gain the guardian's approval")
    elif npc == "guardian" and game.npc_global_flags.get("guardian_met"):
        if "Gain the guardian's approval" in game.quests:
            game.quests.remove("Gain the guardian's approval")

    if (
        game.npc_global_flags.get("dreamer_hint")
        and not game.npc_global_flags.get("dreamer_met")
        and "Seek the dreamer" not in game.quests
    ):
        game.quests.append("Seek the dreamer")
    if (
        game.npc_global_flags.get("mentor_tip")
        and not game.npc_global_flags.get("mentor_met")
        and "Train with the mentor" not in game.quests
    ):
        game.quests.append("Train with the mentor")


def talk(game: "Game", npc: str) -> None:
    """Converse with an NPC if present in the current directory."""
    location = game.npc_locations.get(npc)
    if location != game.current:
        game._output(f"There is no {npc} here.")
        return

    game.active_npc = npc

    dialog_file = game.data_dir / "npc" / f"{npc}.dialog"
    try:
        raw_lines = dialog_file.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        game._output(f"{npc.capitalize()} has nothing to say.")
        return

    sections: list[list[str]] = [[]]
    for line in raw_lines:
        if line.strip() == "---":
            sections.append([])
            continue
        sections[-1].append(line)

    entry = game.npc_state.get(npc, {"section": 0, "flags": {}})
    if isinstance(entry, dict):
        state = entry.get("section", 0)
        flags = entry.get("flags", {})
    else:
        state = int(entry)
        flags = {}
    flags["glitched"] = game.glitch_mode
    combined_flags = dict(game.npc_global_flags)
    combined_flags.update(flags)
    if state >= len(sections):
        state = len(sections) - 1
    lines = sections[state]

    i = 0
    while i < len(lines):
        stripped = lines[i].lstrip()
        if stripped.startswith(">"):
            choices: list[str] = []
            effects: list[list[tuple[str, object]]] = []
            while i < len(lines) and lines[i].lstrip().startswith(">"):
                choice_line = lines[i].lstrip()[1:].strip()
                effect_list: list[tuple[str, object]] = []
                required_item: str | None = None
                if "[" in choice_line and choice_line.endswith("]"):
                    base, meta = choice_line.rsplit("[", 1)
                    choice_line = base.strip()
                    meta = meta[:-1]
                    for piece in meta.split(";"):
                        piece = piece.strip()
                        if not piece:
                            continue
                        if piece.startswith("+"):
                            effect_list.append((piece[1:], True))
                        elif piece.startswith("-"):
                            effect_list.append((piece[1:], False))
                        elif piece.startswith("trust+="):
                            try:
                                amt = int(piece.split("=", 1)[1])
                            except ValueError:
                                amt = 1
                            effect_list.append(("trust_adj", amt))
                        elif piece.startswith("trust-="):
                            try:
                                amt = int(piece.split("=", 1)[1])
                            except ValueError:
                                amt = 1
                            effect_list.append(("trust_adj", -amt))
                        elif piece.startswith("give="):
                            required_item = piece.split("=", 1)[1].strip()
                        elif "=" in piece:
                            k, v = piece.split("=", 1)
                            effect_list.append((k.strip(), v.strip()))
                        else:
                            effect_list.append((piece.strip(), True))
                given_items = entry.get("given", []) if isinstance(entry, dict) else []
                if required_item and required_item not in given_items:
                    i += 1
                    continue
                choices.append(choice_line)
                effects.append(effect_list)
                i += 1
            for idx, choice in enumerate(choices, 1):
                game._output(f"{idx}. {choice}")
            sel = input("> ").strip()
            if sel.isdigit():
                idx = int(sel) - 1
                if 0 <= idx < len(choices):
                    game._output(choices[idx])
                    effect_list = effects[idx]
                    for effect in effect_list:
                        key = effect[0]
                        val = effect[1]
                        if key == "journal":
                            game.journal.append(str(val))
                            continue
                        if key == "trust_adj":
                            game.npc_trust[npc] = game.npc_trust.get(npc, 0) + int(val)
                            continue
                        if key.startswith("g+"):
                            gflag = key[2:]
                            game.npc_global_flags[gflag] = True
                            combined_flags[gflag] = True
                            continue
                        if key.startswith("g-"):
                            gflag = key[2:]
                            game.npc_global_flags[gflag] = False
                            combined_flags[gflag] = False
                            continue
                        flags[key] = val
                        combined_flags[key] = val
            continue
        if stripped.startswith("?"):
            cond, _, text = stripped[1:].partition(":")
            cond = cond.strip()
            negate = cond.startswith("!")
            if negate:
                cond = cond[1:]
            import re
            trust_val = game.npc_trust.get(npc, 0)
            m = re.match(r"trust\s*(>=|<=|==|!=|>|<)\s*(-?\d+)", cond)
            if m:
                op, num = m.group(1), int(m.group(2))
                if op == ">":
                    present = trust_val > num
                elif op == "<":
                    present = trust_val < num
                elif op == ">=":
                    present = trust_val >= num
                elif op == "<=":
                    present = trust_val <= num
                elif op == "==":
                    present = trust_val == num
                else:  # !=
                    present = trust_val != num
            else:
                present = bool(combined_flags.get(cond))
            if present != negate:
                game._output(text.lstrip())
            i += 1
            continue
        game._output(lines[i])
        i += 1

    if state < len(sections) - 1:
        state += 1
    if isinstance(entry, dict):
        given_items = entry.get("given", [])
    else:
        given_items = []
    game.npc_state[npc] = {"section": state, "flags": flags, "given": given_items}
    update_quests_after_talk(game, npc)
