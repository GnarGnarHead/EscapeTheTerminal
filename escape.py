"""Escape the Terminal - minimal command loop.

This module now exposes a :class:`Game` object to make future expansion
easier while preserving the original command-line interface.
"""

from pathlib import Path


class Game:
    """Simple command dispatcher for the terminal adventure."""

    def __init__(self):
        self.inventory = []
        # base filesystem state; the hidden directory is injected when unlocked
        self.hidden_dir = {
            "desc": "A directory shrouded in mystery.",
            "items": ["mem.fragment", "treasure.txt"],
            "dirs": {
                "vault": {
                    "desc": "A locked vault storing plans best kept secret.",
                    "items": ["escape.plan"],
                    "dirs": {},
                }
            },
        }
        self.fs = {
            "desc": (
                "You find yourself in a dimly lit terminal session. "
                "The prompt blinks patiently."
            ),
            "items": ["access.key", "voice.log"],
            "dirs": {
                "lab": {
                    "desc": "A cluttered research lab filled with blinking devices.",
                    "items": ["decoder"],
                    "dirs": {},
                },
                "archive": {
                    "desc": "Dusty shelves of data backups line the walls.",
                    "items": ["old.note"],
                    "dirs": {},
                },
                "core": {
                    "desc": "The core systems thrum with latent energy.",
                    "items": [],
                    "dirs": {
                        "npc": {
                            "desc": "A quiet daemon lingers here, waiting to be addressed.",
                            "items": ["daemon.log"],
                            "dirs": {},
                        }
                    },
                },
                "dream": {
                    "desc": "A hazy directory where reality blurs and ideas take shape.",
                    "items": ["lucid.note"],
                    "dirs": {
                        "subconscious": {
                            "desc": "Half-formed thoughts linger here, waiting to be read.",
                            "items": ["reverie.log"],
                            "dirs": {},
                        },
                        "npc": {
                            "desc": "A soft presence waits to converse in this lucid space.",
                            "items": [],
                            "dirs": {},
                        },
                    },
                },
                "memory": {
                    "desc": "Stacks of recollections archived for later reflection.",
                    "items": ["flashback.log"],
                    "dirs": {},
                },
            },
        }
        self.current = []  # path as list of directory names
        self.npc_locations = {
            "daemon": ["core", "npc"],
            "dreamer": ["dream", "npc"],
        }
        # track dialogue progress for each NPC
        self.npc_state: dict[str, int] = {}
        self.item_descriptions = {
            "access.key": "A slim digital token rumored to unlock hidden directories.",
            "treasure.txt": "A file filled with untold riches.",
            "mem.fragment": "A corrupted memory fragment pulsing faintly with data.",
            "voice.log": "An audio log that might contain a clue.",
            "decoder": "A handheld device used to decode encrypted signals.",
            "old.note": "A weathered note scribbled with barely readable commands.",
            "daemon.log": "A log file chronicling the mutterings of a resident daemon.",
            "lucid.note": "A scribbled note describing techniques for conscious dreaming.",
            "flashback.log": "A recorded memory playback waiting to be relived.",
            "reverie.log": "A log capturing fleeting reveries within the system.",
            "escape.plan": "A hastily sketched route promising a way out.",
            "escape.code": "A brief sequence hinting at a path to freedom.",
        }
        # populate multiple directories with extra procedurally generated content
        self._generate_extra_dirs(["dream", "memory", "core"])
        self.use_messages = {
            "access.key": "The key hums softly and a hidden directory flickers into view.",
            "mem.fragment": "Fragments of your past flash before your eyes.",
            "voice.log": "A haunting voice whispers: 'Find the fragment.'",
            "daemon.log": "The daemon rasps from deep within the system: 'Keep your code clean.'",
            "lucid.note": "The words resonate, sharpening your awareness of the dream.",
            "flashback.log": "Memories surge forth, revealing forgotten paths.",
        }
        self.save_file = "game.sav"
        self.data_dir = Path(__file__).parent / "data"
        self.glitch_mode = False
        self.glitch_steps = 0

        # directory for autogenerated log files
        self.logs_path = self.data_dir / "logs"
        self._generate_logs()

        # map commands and aliases to handler callables
        self.command_map = {
            "help": lambda arg="": self._print_help(),
            "h": lambda arg="": self._print_help(),
            "look": lambda arg="": self._look(),
            "look around": lambda arg="": self._look(),
            "ls": lambda arg="": self._ls(),
            "pwd": lambda arg="": self._pwd(),
            "cd": lambda arg="": self._cd(arg),
            "take": lambda arg="": self._take(arg),
            "drop": lambda arg="": self._drop(arg),
            "inventory": lambda arg="": self._inventory(),
            "inv": lambda arg="": self._inventory(),
            "i": lambda arg="": self._inventory(),
            "examine": lambda arg="": self._examine(arg),
            "use": lambda arg="": self._use_command(arg),
            "cat": lambda arg="": self._cat(arg),
            "grep": lambda arg="": self._grep(arg),
            "decode": lambda arg="": self._decode(arg),
            "talk": lambda arg="": self._talk(arg),
            "map": lambda arg="": self._map(),
            "save": lambda arg="": self._save(arg),
            "load": lambda arg="": self._load(arg),
            "glitch": lambda arg="": self._toggle_glitch(),
            "quit": lambda arg="": self._quit(),
            "exit": lambda arg="": self._quit(),
        }

    def _generate_extra_dirs(self, bases: list[str] | str = "dream") -> None:
        """Populate directories under each base path with random subdirectories."""
        import os
        import random

        if isinstance(bases, str):
            bases = [bases]

        seed_val = os.getenv("ET_EXTRA_SEED")
        rnd = random.Random(int(seed_val)) if seed_val is not None else random.Random()

        adjectives = ["misty", "vivid", "neon", "echoing"]
        nouns = ["hall", "nexus", "alcove", "node"]
        item_defs = [
            ("dream.shard", "A sliver of surreal memory."),
            ("echo.bit", "An echo of a forgotten idea."),
            ("vision.chip", "A chip flickering with ephemeral scenes."),
        ]
        for base in bases:
            base_node = self.fs["dirs"].get(base)
            if not base_node:
                continue

            count = rnd.randint(2, 3)
            for idx in range(count):
                dname = f"{rnd.choice(adjectives)}_{rnd.choice(nouns)}_{idx}"
                desc = (
                    f"A {rnd.choice(['strange', 'fleeting', 'curious'])} place within the dream."
                )
                items: list[str] = []
                if rnd.random() < 0.5:
                    it_name, it_desc = rnd.choice(item_defs)
                    it_name = it_name.replace(".", f"{idx}.")
                    items.append(it_name)
                    self.item_descriptions[it_name] = it_desc
                base_node["dirs"][dname] = {"desc": desc, "items": items, "dirs": {}}

    def _generate_logs(self) -> None:
        """Create the logs directory with random log files."""
        import os
        import random

        self.logs_path.mkdir(exist_ok=True)
        for old in self.logs_path.glob('*.log'):
            try:
                old.unlink()
            except OSError:
                pass
        seed_val = os.getenv("ET_EXTRA_SEED")
        rnd = random.Random(int(seed_val)) if seed_val is not None else random.Random()

        count = rnd.randint(3, 5)
        files: list[str] = []
        for i in range(count):
            fname = f"system_{rnd.randint(1000,9999)}.log"
            files.append(fname)
            lines = [
                f"INFO iteration {i}",
                "SYSTEM BOOT COMPLETE" if i == 0 else f"DEBUG value {rnd.randint(0,100)}",
            ]
            with open(self.logs_path / fname, "w", encoding="utf-8") as f:
                f.write("\n".join(lines) + "\n")

        self.fs["dirs"]["logs"] = {"desc": "System logs are stored here.", "items": files, "dirs": {}}
        for name in files:
            self.item_descriptions.setdefault(name, "A cryptic system log file.")

    def _toggle_glitch(self):
        self.glitch_mode = not self.glitch_mode
        state = "activated" if self.glitch_mode else "deactivated"
        if not self.glitch_mode:
            self.glitch_steps = 0
        print(f"Glitch mode {state}.")

    def _output(self, text: str = "") -> None:
        """Print text, applying glitch effects when enabled."""
        if self.glitch_mode and text:
            self.glitch_steps += 1
            text = self._glitch_text(text, self.glitch_steps)
            import random
            rnd = random.Random(self.glitch_steps * 42)
            if self.glitch_steps in (3, 6, 9):
                msg = rnd.choice([
                    "-- SYSTEM CORRUPTION --",
                    "** SIGNAL LOST **",
                    "[memory anomaly]",
                ])
                print(msg)
            if rnd.random() < 0.2:
                noise = rnd.choice(["...glitch...", "~~~", "<!>"])
                print(noise)
        print(text)

    def _glitch_text(self, text: str, step: int) -> str:
        """Return ``text`` with deterministic corruption based on ``step``."""
        import random
        import hashlib

        key = f"{text}-{step}".encode()
        seed = int.from_bytes(hashlib.sha256(key).digest()[:4], "little")
        rnd = random.Random(seed)

        prob = min(0.15 + step * 0.07, 0.8)
        word_prob = 0.0
        if step > 3:
            word_prob = min((step - 3) * 0.05, 0.3)

        words = text.split()
        for i, w in enumerate(words):
            if rnd.random() < word_prob:
                words[i] = "".join(rnd.choice("@#$%&*") for _ in w)
        text = " ".join(words)

        chars = list(text)
        for i, ch in enumerate(chars):
            if ch.isalpha() and rnd.random() < prob:
                chars[i] = rnd.choice("@#$%&*")
        return "".join(chars)

    def _print_help(self):
        self._output(
            "Available commands: help, look, ls, cd <dir>, pwd, take <item>, drop <item>, "
            "inventory, examine <item>, use <item> [on <target>], cat <file>, talk <npc>, save [slot], load [slot], glitch, quit"
        )

    def _current_node(self):
        node = self.fs
        for part in self.current:
            node = node["dirs"][part]
        return node

    def _look(self):
        node = self._current_node()
        self._output(node["desc"])
        entries = [d + "/" for d in node["dirs"]] + list(node["items"])
        if entries:
            self._output("You see: " + ", ".join(entries))

    def _take(self, item: str):
        node = self._current_node()
        if item in node["items"]:
            node["items"].remove(item)
            self.inventory.append(item)
            self._output(f"You pick up the {item}.")
        else:
            self._output(f"There is no {item} here.")

    def _drop(self, item: str):
        if item in self.inventory:
            self.inventory.remove(item)
            node = self._current_node()
            node["items"].append(item)
            self._output(f"You drop the {item}.")
        else:
            self._output(f"You do not have {item} to drop.")

    def _inventory(self):
        if self.inventory:
            self._output("Inventory: " + ", ".join(self.inventory))
        else:
            self._output("Inventory is empty.")

    def _examine(self, item: str):
        node = self._current_node()
        if item in self.inventory or item in node["items"]:
            desc = self.item_descriptions.get(item, "It's unremarkable.")
            self._output(desc)
        else:
            self._output(f"You do not have {item} to examine.")

    def _use(self, item: str, target: str | None = None):
        if item not in self.inventory:
            self._output(f"You do not have {item} to use.")
            return

        # item on target interactions
        if item == "access.key" and (target == "door" or target is None):
            root = self.fs
            if "hidden" not in root["dirs"]:
                root["dirs"]["hidden"] = self.hidden_dir
            msg = self.use_messages.get(item)
            if msg:
                self._output(msg)
            return
        if item == "decoder" and target == "mem.fragment":
            self._decode("mem.fragment")
            return
        if target:
            self._output(f"You try to use {item} on {target} but nothing happens.")
            return

        msg = self.use_messages.get(item)
        if msg:
            self._output(msg)
        else:
            self._output(f"You can't use {item} right now.")

    def _use_command(self, arg: str) -> None:
        """Parse arguments for the ``use`` command and dispatch to :meth:`_use`."""
        use_args = arg
        if " on " in use_args:
            item_part, target = use_args.split(" on ", 1)
            item = item_part.strip()
            target = target.strip()
        else:
            item = use_args.strip()
            target = None
        if item:
            self._use(item, target)

    def _decode(self, item: str) -> None:
        target = item.strip()
        if target != "mem.fragment":
            self._output(f"Don't know how to decode {target}.")
            return
        if "decoder" not in self.inventory:
            self._output("You need the decoder to decode the fragment.")
            return
        if target not in self.inventory:
            self._output(f"You do not have {target} to decode.")
            return
        self.inventory.remove(target)
        vault = self.hidden_dir["dirs"]["vault"]
        if "escape" not in vault["dirs"]:
            vault["dirs"]["escape"] = {
                "desc": "A compartment revealed by decoding the fragment.",
                "items": ["escape.code"],
                "dirs": {},
            }
        self._output(
            "The decoder hums and a new directory appears within hidden/vault."
        )

    def _cat(self, filename: str):
        path = self.data_dir / filename
        try:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
        except FileNotFoundError:
            self._output(f"No such file: {filename}")
            return
        except OSError as e:
            self._output(f"Failed to read {filename}: {e}")
            return
        self._output(text.rstrip())
        if filename == "daemon.log":
            msg = self.use_messages.get("daemon.log")
            if msg:
                self._output(msg)

    def _grep(self, pattern: str) -> None:
        """Print lines from log files matching ``pattern``."""
        import re

        if not pattern:
            self._output("Usage: grep <pattern>")
            return
        regex = re.compile(pattern, re.IGNORECASE)
        found = False
        for path in sorted(self.logs_path.glob("*.log")):
            try:
                lines = path.read_text(encoding="utf-8").splitlines()
            except OSError:
                continue
            for line in lines:
                if regex.search(line):
                    self._output(f"{path.name}: {line}")
                    found = True
        if not found:
            self._output("No matches found.")

    def _talk(self, npc: str):
        """Converse with an NPC if present in the current directory."""
        location = self.npc_locations.get(npc)
        if location != self.current:
            self._output(f"There is no {npc} here.")
            return

        dialog_file = self.data_dir / "npc" / f"{npc}.dialog"
        try:
            raw_lines = dialog_file.read_text(encoding="utf-8").splitlines()
        except FileNotFoundError:
            self._output(f"{npc.capitalize()} has nothing to say.")
            return

        sections: list[list[str]] = [[]]
        for line in raw_lines:
            if line.strip() == "---":
                sections.append([])
                continue
            sections[-1].append(line)

        state = self.npc_state.get(npc, 0)
        if state >= len(sections):
            state = len(sections) - 1
        lines = sections[state]

        i = 0
        while i < len(lines):
            if lines[i].lstrip().startswith(">"):
                choices = []
                while i < len(lines) and lines[i].lstrip().startswith(">"):
                    choices.append(lines[i].lstrip()[1:].strip())
                    i += 1
                for idx, choice in enumerate(choices, 1):
                    self._output(f"{idx}. {choice}")
                sel = input("> ").strip()
                if sel.isdigit():
                    idx = int(sel) - 1
                    if 0 <= idx < len(choices):
                        self._output(choices[idx])
                continue
            self._output(lines[i])
            i += 1

        if state < len(sections) - 1:
            self.npc_state[npc] = state + 1
        else:
            self.npc_state[npc] = state

    def _ls(self):
        node = self._current_node()
        entries = [d + '/' for d in node['dirs']] + list(node['items'])
        if entries:
            self._output(" ".join(entries))
        else:
            self._output("Nothing here.")

    def _map(self, node: dict | None = None, prefix: str = "") -> None:
        """Recursively display the tree from ``node`` or the current directory."""
        if node is None:
            node = self._current_node()
            self._output(".")

        entries = list(node.get("dirs", {}).keys()) + list(node.get("items", []))
        for idx, name in enumerate(entries):
            is_last = idx == len(entries) - 1
            connector = "└── " if is_last else "├── "
            if name in node.get("dirs", {}):
                self._output(f"{prefix}{connector}{name}/")
                next_prefix = f"{prefix}    " if is_last else f"{prefix}│   "
                self._map(node["dirs"][name], next_prefix)
            else:
                self._output(f"{prefix}{connector}{name}")

    def _pwd(self):
        path = '/'.join(self.current) if self.current else '/'
        self._output(path)

    def _cd(self, directory: str):
        if directory in ('.', ''):
            return
        if directory == '..':
            if self.current:
                self.current.pop()
            else:
                self._output("Already at root.")
            return
        node = self._current_node()
        if directory in node['dirs']:
            self.current.append(directory)
        else:
            self._output(f"No such directory: {directory}")

    def _save(self, slot: str = ""):
        """Save game state to ``game<slot>.sav`` (default ``game.sav``)."""
        fname = self.save_file if not slot else f"game{slot}.sav"
        data = {
            "fs": self.fs,
            "inventory": self.inventory,
            "current": self.current,
            "glitch_mode": self.glitch_mode,
            "glitch_steps": self.glitch_steps,
            "npc_state": self.npc_state,
        }
        try:
            with open(fname, "w", encoding="utf-8") as f:
                import json

                json.dump(data, f)
        except OSError as e:
            self._output(f"Failed to save: {e}")
        else:
            self._output("Game saved.")

    def _load(self, slot: str = ""):
        """Load game state from ``game<slot>.sav`` (default ``game.sav``)."""
        fname = self.save_file if not slot else f"game{slot}.sav"
        import json

        try:
            with open(fname, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            self._output("No save file found.")
            return
        except OSError as e:
            self._output(f"Failed to load: {e}")
            return
        self.fs = data.get("fs", self.fs)
        self.inventory = data.get("inventory", [])
        self.current = data.get("current", [])
        self.glitch_mode = data.get("glitch_mode", False)
        self.glitch_steps = data.get("glitch_steps", 0)
        self.npc_state = data.get("npc_state", {})
        self._output("Game loaded.")

    def _quit(self) -> bool:
        """Print exit message and signal the main loop to stop."""
        self._output("Goodbye")
        return True

    def run(self):
        self._output("Welcome to Escape the Terminal")
        self._output("Type 'help' for a list of commands. Type 'quit' to exit.")
        while True:
            try:
                cmd = input('> ').strip().lower()
            except EOFError:
                self._output()
                break
            if not cmd:
                continue

            handler = self.command_map.get(cmd)
            if handler is None:
                parts = cmd.split(' ', 1)
                base = parts[0]
                arg = parts[1] if len(parts) > 1 else ''
                handler = self.command_map.get(base)
            else:
                arg = ''

            if handler:
                should_quit = handler(arg)
                if should_quit:
                    break
            else:
                self._output(f"Unknown command: {cmd}")


def main():
    Game().run()


if __name__ == '__main__':
    main()
