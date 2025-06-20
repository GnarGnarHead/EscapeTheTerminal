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
            "dirs": {},
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
                    "dirs": {},
                },
                "memory": {
                    "desc": "Stacks of recollections archived for later reflection.",
                    "items": ["flashback.log"],
                    "dirs": {},
                },
            },
        }
        self.current = []  # path as list of directory names
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
        }
        # populate the dream directory with extra procedurally generated content
        self._generate_extra_dirs()
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

    def _generate_extra_dirs(self, base: str = "dream") -> None:
        """Populate ``base`` directory with random subdirectories."""
        import os
        import random

        seed_val = os.getenv("ET_EXTRA_SEED")
        rnd = random.Random(int(seed_val)) if seed_val is not None else random.Random()

        base_node = self.fs["dirs"].get(base)
        if not base_node:
            return

        adjectives = ["misty", "vivid", "neon", "echoing"]
        nouns = ["hall", "nexus", "alcove", "node"]
        item_defs = [
            ("dream.shard", "A sliver of surreal memory."),
            ("echo.bit", "An echo of a forgotten idea."),
            ("vision.chip", "A chip flickering with ephemeral scenes."),
        ]

        count = rnd.randint(2, 3)
        for idx in range(count):
            dname = f"{rnd.choice(adjectives)}_{rnd.choice(nouns)}_{idx}"
            desc = f"A {rnd.choice(['strange', 'fleeting', 'curious'])} place within the dream."
            items: list[str] = []
            if rnd.random() < 0.5:
                it_name, it_desc = rnd.choice(item_defs)
                it_name = it_name.replace(".", f"{idx}.")
                items.append(it_name)
                self.item_descriptions[it_name] = it_desc
            base_node["dirs"][dname] = {"desc": desc, "items": items, "dirs": {}}

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
            # occasionally insert additional glitch noise
            import random
            rnd = random.Random(self.glitch_steps * 42)
            if rnd.random() < 0.2:
                noise = rnd.choice(["...glitch...", "~~~", "<!>"])
                print(noise)
        print(text)

    def _glitch_text(self, text: str, step: int) -> str:
        import random
        import hashlib

        key = f"{text}-{step}".encode()
        seed = int.from_bytes(hashlib.sha256(key).digest()[:4], "little")
        rnd = random.Random(seed)
        prob = min(0.1 + step * 0.05, 0.6)
        chars = list(text)
        for i, ch in enumerate(chars):
            if ch.isalpha() and rnd.random() < prob:
                chars[i] = rnd.choice("@#$%&*")
        return "".join(chars)

    def _print_help(self):
        self._output(
            "Available commands: help, look, ls, cd <dir>, pwd, take <item>, drop <item>, "
            "inventory, examine <item>, use <item> [on <target>], cat <file>, talk <npc>, save, load, glitch, quit"
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
            self._output("The decoder reveals a secret exit command within the fragment.")
            return
        if target:
            self._output(f"You try to use {item} on {target} but nothing happens.")
            return

        msg = self.use_messages.get(item)
        if msg:
            self._output(msg)
        else:
            self._output(f"You can't use {item} right now.")

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

    def _talk(self, npc: str):
        """Converse with an NPC if present in the current directory."""
        if npc == "daemon":
            if self.current != ["core", "npc"]:
                self._output("There is no daemon here.")
                return
            dialog_file = self.data_dir / "npc" / "daemon.dialog"
        else:
            self._output(f"There is no {npc} here.")
            return

        try:
            with open(dialog_file, "r", encoding="utf-8") as f:
                for line in f:
                    self._output(line.rstrip())
        except FileNotFoundError:
            self._output(f"{npc.capitalize()} has nothing to say.")

    def _ls(self):
        node = self._current_node()
        entries = [d + '/' for d in node['dirs']] + list(node['items'])
        if entries:
            self._output(" ".join(entries))
        else:
            self._output("Nothing here.")

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

    def _save(self):
        data = {
            "fs": self.fs,
            "inventory": self.inventory,
            "current": self.current,
        }
        try:
            with open(self.save_file, "w", encoding="utf-8") as f:
                import json

                json.dump(data, f)
        except OSError as e:
            self._output(f"Failed to save: {e}")
        else:
            self._output("Game saved.")

    def _load(self):
        import json

        try:
            with open(self.save_file, "r", encoding="utf-8") as f:
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
        self._output("Game loaded.")

    def run(self):
        self._output("Welcome to Escape the Terminal")
        self._output("Type 'help' for a list of commands. Type 'quit' to exit.")
        while True:
            try:
                cmd = input('> ').strip().lower()
            except EOFError:
                self._output()
                break
            if cmd in ('help', 'h'):
                self._print_help()
            elif cmd in ('look', 'look around'):
                self._look()
            elif cmd == 'ls':
                self._ls()
            elif cmd == 'pwd':
                self._pwd()
            elif cmd.startswith('cd'):
                directory = cmd.split(' ', 1)[1] if ' ' in cmd else ''
                self._cd(directory)
            elif cmd.startswith('take '):
                item = cmd.split(' ', 1)[1]
                self._take(item)
            elif cmd.startswith('drop '):
                item = cmd.split(' ', 1)[1]
                self._drop(item)
            elif cmd in ('inventory', 'inv', 'i'):
                self._inventory()
            elif cmd.startswith('examine '):
                item = cmd.split(' ', 1)[1]
                self._examine(item)
            elif cmd.startswith('use '):
                use_args = cmd[4:]
                if ' on ' in use_args:
                    item_part, target = use_args.split(' on ', 1)
                    item = item_part.strip()
                    target = target.strip()
                else:
                    item = use_args.strip()
                    target = None
                self._use(item, target)
            elif cmd.startswith('cat '):
                filename = cmd.split(' ', 1)[1]
                self._cat(filename)
            elif cmd.startswith('talk '):
                npc = cmd.split(' ', 1)[1]
                self._talk(npc)
            elif cmd == 'save':
                self._save()
            elif cmd == 'load':
                self._load()
            elif cmd == 'glitch':
                self._toggle_glitch()
            elif cmd in ('quit', 'exit'):
                self._output("Goodbye")
                break
            elif not cmd:
                continue
            else:
                self._output(f"Unknown command: {cmd}")


def main():
    Game().run()


if __name__ == '__main__':
    main()
