"""Escape the Terminal - minimal command loop.

This module now exposes a :class:`Game` object to make future expansion
easier while preserving the original command-line interface.
"""

from __future__ import annotations

from pathlib import Path
import os
import json
from enum import IntEnum

from . import commands, filesystem, npc as npc_module


class StoryPhase(IntEnum):
    """High level story progression."""

    INTRO = 0
    LOGS_READ = 1
    RUNTIME_UNLOCKED = 2
    ENDGAME = 3


class Game:
    """Simple command dispatcher for the terminal adventure."""

    MAX_CORRUPTION = 400

    def _corruption_percent(self) -> int:
        return min(int(self.corruption * 100 / self.MAX_CORRUPTION), 100)

    REQUIRED_ITEMS = {
        "node3": "firmware.patch",
        "node4": "root.access",
        "node5": "super.user",
        "node6": "admin.override",
        "node7": "kernel.key",
        "node8": "master.process",
        "node9": "hypervisor.command",
        "node10": "quantum.access",
        "node11": "quantum.override",
        "node12": "guardian.key",
        "runtime": "kernel.key",
    }

    def __init__(
        self,
        use_color: bool | None = None,
        world_file: str | Path | None = None,
        prompt: str | None = None,
    ):
        if use_color is None:
            env_val = os.getenv("ET_COLOR", "0").lower()
            self.use_color = env_val not in ("0", "false", "")
        else:
            self.use_color = use_color

        env_dir = os.getenv("ET_COLOR_DIR")
        self.dir_color = f"\x1b[{env_dir}m" if env_dir else "\x1b[33m"
        env_item = os.getenv("ET_COLOR_ITEM")
        self.item_color = f"\x1b[{env_item}m" if env_item else "\x1b[36m"

        self.auto_save = os.getenv("ET_AUTOSAVE") not in (None, "", "0", "false")
        self.prompt = prompt if prompt is not None else os.getenv("ET_PROMPT", "> ")
        self.inventory = []
        self.visited_dirs: set[str] = {'/'}
        self.collected_items: set[str] = set()
        self.score = 0
        self.achievements: list[str] = []
        self.data_dir = Path(__file__).parent / "data"
        if world_file is None:
            world_file = self.data_dir / "world.json"
        with open(world_file, "r", encoding="utf-8") as f:
            world = json.load(f)
        self.fs = world.get("fs", {})
        self._base_root_desc = self.fs.get("desc", "")
        self.hidden_dir = world.get("hidden_dir", {})
        self.network_node = world.get("network_node", {})
        self.deep_network_node = world.get("deep_network_node", {})
        self.npc_locations = world.get("npc_locations", {})
        self.item_descriptions = world.get("item_descriptions", {})
        self.recipes = world.get("recipes", {})
        self.current = []  # path as list of directory names
        # track dialogue progress and flags for each NPC
        self.npc_state: dict[str, dict] = {}
        # flags that apply to all NPCs based on achievements
        self.npc_global_flags: dict[str, bool] = {}
        # per-NPC trust levels for conditional dialog
        self.npc_trust: dict[str, int] = {}
        # story progression stage for unlocking features
        self.progress_stage = 0
        self.story_phase = StoryPhase.INTRO
        # expose the Enum on the instance for NPC modules
        self.StoryPhase = StoryPhase
        self.use_messages = {
            "access.key": "The key hums softly and a hidden directory flickers into view.",
            "mem.fragment": "Fragments of your past flash before your eyes.",
            "voice.log": "A haunting voice whispers: 'Find the fragment.'",
            "daemon.log": "The daemon rasps from deep within the system: 'Keep your code clean.'",
            "lucid.note": "The words resonate, sharpening your awareness of the dream.",
            "flashback.log": "Memories surge forth, revealing forgotten paths.",
        }
        self.save_file = "game.sav"
        env_save_dir = os.getenv("ET_SAVE_DIR")
        self.save_dir = Path(env_save_dir) if env_save_dir else Path.cwd()
        self.glitch_mode = False
        self.glitch_steps = 0

        # emotional state tracking
        self.emotion_state = "confused"
        self._prev_emotion_state = self.emotion_state
        self._memory_emotions = {"memory8.log": "alarmed", "memory11.log": "hopeful"}

        # store all commands the player enters this session
        self.command_history: list[str] = []

        # notes recorded by the player
        self.journal: list[str] = []

        # active quests tracked by the player
        self.quests: list[str] = []
        # begin with an initial quest
        self.quests.append("Recover your lost memory")

        # system corruption counter
        self.corruption = 0
        self._corruption_stage = 0

        # runtime command aliases created via the 'alias' command
        self.aliases: dict[str, str] = {}

        # names of plugin modules successfully loaded
        self.loaded_plugins: list[str] = []

        # NPC currently in conversation
        self.active_npc: str | None = None

        # directory for autogenerated log files
        self.logs_path = self.data_dir / "logs"
        filesystem.generate_logs(self)

        # descriptions for help output
        self.command_descriptions = commands.COMMAND_DESCRIPTIONS.copy()

        # map commands and aliases to handler callables
        self.command_map = commands.build_command_map(self)

        # discover and load optional plugin modules
        self._load_plugins()

    def advance_phase(self, phase: StoryPhase) -> None:
        """Move to ``phase`` if it is higher than the current story phase."""
        if phase > self.story_phase:
            self.story_phase = phase

    def _generate_extra_dirs(self, bases: list[str] | str = "dream") -> None:
        """Populate directories under each base path with random subdirectories."""
        filesystem.generate_extra_dirs(self, bases)

    def _generate_logs(self) -> None:
        """Create the logs directory with random log files."""
        filesystem.generate_logs(self)

    def _load_plugins(self) -> None:
        """Import plugin modules from built-in and custom plugin directories."""
        import importlib.util
        import sys
        import zipimport

        builtin_dir = Path(__file__).parent / "plugins"
        plugin_dirs = []
        if builtin_dir.is_dir():
            plugin_dirs.append(builtin_dir)

        extra_paths = os.getenv("ET_PLUGIN_PATH")
        if extra_paths:
            for p in extra_paths.split(os.pathsep):
                if not p:
                    continue
                path = Path(p)
                if path.is_dir():
                    plugin_dirs.append(path)

        for plugins_dir in plugin_dirs:
            # load regular Python files
            for path in plugins_dir.glob("*.py"):
                if path.name.startswith("__"):
                    continue
                if plugins_dir == builtin_dir:
                    module_name = f"escape.plugins.{path.stem}"
                else:
                    module_name = path.stem
                spec = importlib.util.spec_from_file_location(module_name, path)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    module.game = self
                    sys.modules[module_name] = module
                    try:
                        spec.loader.exec_module(module)
                        self.loaded_plugins.append(module_name)
                    except Exception as exc:
                        print(f"Failed to load plugin {path.name}: {exc}")

            # load zipped plugins
            for path in plugins_dir.glob("*.zip"):
                if plugins_dir == builtin_dir:
                    module_name = f"escape.plugins.{path.stem}"
                else:
                    module_name = path.stem
                try:
                    importer = zipimport.zipimporter(str(path))
                except zipimport.ZipImportError as exc:
                    print(f"Failed to read plugin {path.name}: {exc}")
                    continue
                spec = importlib.util.spec_from_loader(module_name, importer)
                if spec and spec.loader:
                    try:
                        if hasattr(importer, "exec_module"):
                            module = importlib.util.module_from_spec(spec)
                            module.game = self
                            sys.modules[module_name] = module
                            importer.exec_module(module)
                            self.loaded_plugins.append(module_name)
                        else:
                            # zipimporter on older Python versions lacks exec_module
                            # so we manually execute the plugin code with the game
                            # instance available in globals
                            import zipfile

                            with zipfile.ZipFile(path) as zf:
                                target = f"{path.stem}.py"
                                if target in zf.namelist():
                                    source = zf.read(target).decode("utf-8")
                                else:
                                    raise FileNotFoundError(
                                        f"{target} not found in {path.name}"
                                    )

                            module = importlib.util.module_from_spec(spec)
                            module.game = self
                            sys.modules[module_name] = module
                            exec(compile(source, target, "exec"), module.__dict__)
                            self.loaded_plugins.append(module_name)
                    except Exception as exc:
                        print(f"Failed to load plugin {path.name}: {exc}")

    def _toggle_glitch(self):
        self.glitch_mode = not self.glitch_mode
        state = "activated" if self.glitch_mode else "deactivated"
        if self.glitch_mode:
            if "glitch_root" not in self.fs.get("dirs", {}):
                self.fs.setdefault("dirs", {})["glitch_root"] = {
                    "desc": "A distorted mirror of the filesystem.",
                    "items": [".ghost"],
                    "dirs": {
                        "false": {
                            "desc": "A directory that denies its own existence.",
                            "items": ["root"],
                            "dirs": {},
                        }
                    },
                }
                self.item_descriptions.setdefault(
                    ".ghost", "A hidden presence phasing in and out of reality."
                )
                self.item_descriptions.setdefault(
                    "root", "An impossible file claiming to be the root."
                )
        else:
            self.glitch_steps = 0
            self.fs.get("dirs", {}).pop("glitch_root", None)
            if self.current and self.current[0] == "glitch_root":
                self.current = []
        print(f"Glitch mode {state}.")

    def _color(self, arg: str = "") -> None:
        """Enable, disable, or toggle ANSI color output."""
        arg = arg.strip().lower()
        if not arg or arg == "toggle":
            self.use_color = not self.use_color
        elif arg == "on":
            self.use_color = True
        elif arg == "off":
            self.use_color = False
        else:
            self._output("Usage: color [on|off|toggle]")
            return
        state = "enabled" if self.use_color else "disabled"
        self._output(f"Color {state}.")

    def _prompt(self, arg: str = "") -> None:
        """Change or show the current input prompt."""
        text = arg
        if text.strip():
            self.prompt = text
            self._output(f"Prompt set to {self.prompt}")
        else:
            self._output(self.prompt)

    def _plugins(self) -> None:
        """Display the names of loaded plugin modules."""
        if self.loaded_plugins:
            for name in self.loaded_plugins:
                self._output(name)
        else:
            self._output("No plugins loaded.")

    def _output(self, text: str = "") -> None:
        """Print ``text`` applying corruption and glitch effects."""
        if self.emotion_state != self._prev_emotion_state:
            print(f"(You feel {self.emotion_state}.)")
            self._prev_emotion_state = self.emotion_state
        pct = self._corruption_percent()
        if pct >= 75 and self._corruption_stage < 3:
            print("-- CORRUPTION 75% --")
            self._corruption_stage = 3
        elif pct >= 50 and self._corruption_stage < 2:
            print("-- CORRUPTION 50% --")
            self._corruption_stage = 2
        elif pct >= 25 and self._corruption_stage < 1:
            print("-- CORRUPTION 25% --")
            self._corruption_stage = 1
        if self.glitch_mode and text:
            self.glitch_steps += 1
            text = self._glitch_text(text, self.glitch_steps)
            import random

            rnd = random.Random(self.glitch_steps * 42)
            if self.glitch_steps in (3, 6, 9):
                msg = rnd.choice(
                    [
                        "-- SYSTEM CORRUPTION --",
                        "** SIGNAL LOST **",
                        "[memory anomaly]",
                    ]
                )
                print(msg)
            if rnd.random() < 0.2:
                noise = rnd.choice(["...glitch...", "~~~", "<!>"])
                print(noise)
            self._apply_glitch_effects()
        if text:
            text = self._apply_corruption(text)
        if self.use_color and text:
            text = self._apply_colors(text)
        print(text)

    def _apply_glitch_effects(self) -> None:
        """Mutate the filesystem when glitch intensity crosses thresholds."""
        root_items = self.fs.setdefault("items", [])
        root_dirs = self.fs.setdefault("dirs", {})
        if self.glitch_mode and "glitch_root" not in root_dirs:
            root_dirs["glitch_root"] = {
                "desc": "A distorted mirror of the filesystem.",
                "items": [".ghost"],
                "dirs": {
                    "false": {
                        "desc": "A directory that denies its own existence.",
                        "items": ["root"],
                        "dirs": {},
                    }
                },
            }
            self.item_descriptions.setdefault(
                ".ghost", "A hidden presence phasing in and out of reality."
            )
            self.item_descriptions.setdefault(
                "root", "An impossible file claiming to be the root."
            )
        if self.glitch_steps == 12:
            self._output(
                "For a split second a directory named 'beyond/' blinks into existence then fades."
            )
            self.glitch_steps -= 1
        if self.glitch_steps == 18:
            self._output(
                "A phantom file 'escape.exe' materializes before dissolving back into nothingness."
            )
            self.glitch_steps -= 1
        if self.glitch_steps >= 5 and "glitch.note" not in root_items:
            root_items.append("glitch.note")
            self.item_descriptions["glitch.note"] = "A fragment of corrupted data."
        if self.glitch_steps >= 10:
            if "glitch.note" in root_items:
                root_items.remove("glitch.note")
        if self.glitch_steps >= 15 and "lab" in self.fs.get("dirs", {}):
            self.fs["dirs"]["lab_glt"] = self.fs["dirs"].pop("lab")
            for npc, path in self.npc_locations.items():
                if path and path[0] == "lab":
                    path[0] = "lab_glt"
        if self.glitch_steps >= 20:
            import random

            rnd = random.Random(self.glitch_steps)
            rnd.shuffle(root_items)
        if self.glitch_steps >= 25 and "glitcher" not in self.npc_locations:
            self.npc_locations["glitcher"] = ["core", "npc"]

        self.fs["desc"] = self._base_root_desc + self._corruption_status()

    def _corruption_status(self) -> str:
        if self.glitch_steps >= 25:
            return " (fractured reality)"
        if self.glitch_steps >= 20:
            return " (unstable system)"
        if self.glitch_steps >= 10:
            return " (corrupted)"
        return ""

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

    def _apply_corruption(self, text: str) -> str:
        """Return ``text`` scrambled according to corruption level."""
        pct = self._corruption_percent()
        if pct < 25:
            return text

        if pct < 50:
            prob = 0.1
        elif pct < 75:
            prob = 0.3
        else:
            prob = 0.6

        import random
        import hashlib

        key = f"{self.corruption}-{text}".encode()
        seed = int.from_bytes(hashlib.sha256(key).digest()[:4], "little")
        rnd = random.Random(seed)

        chars = list(text)
        for i, ch in enumerate(chars):
            if ch.isalpha() and rnd.random() < prob:
                chars[i] = rnd.choice("@#$%&*")
        return "".join(chars)

    def _apply_colors(self, text: str) -> str:
        """Return ``text`` with ANSI colors for items and directories."""
        dirs, items = self._collect_names()
        dir_color = getattr(self, "dir_color", "\x1b[33m")
        item_color = getattr(self, "item_color", "\x1b[36m")
        for name in sorted(dirs, key=len, reverse=True):
            text = text.replace(f"{name}/", f"{dir_color}{name}/\x1b[0m")
        for name in sorted(items, key=len, reverse=True):
            text = text.replace(name, f"{item_color}{name}\x1b[0m")
        return text

    def _collect_names(self) -> tuple[set[str], set[str]]:
        dirs: set[str] = set()
        items: set[str] = set()

        def walk(node: dict) -> None:
            for dname, sub in node.get("dirs", {}).items():
                dirs.add(dname)
                walk(sub)
            for item in node.get("items", []):
                items.add(item)

        walk(self.fs)
        return dirs, items

    def _print_help(self, command: str | None = None) -> None:
        """Display general help or info for a specific command."""
        if command:
            desc = self.command_descriptions.get(command)
            if desc:
                self._output(f"{command}: {desc}")
            else:
                self._output(f"No help available for '{command}'.")
            return

        self._output("Available commands:")
        for cmd in sorted(self.command_descriptions):
            desc = self.command_descriptions[cmd]
            self._output(f"{cmd}: {desc}")

    def _current_node(self):
        return filesystem.current_node(self)

    def _look(self, directory: str = "") -> None:
        filesystem.look(self, directory)

    def _take(self, item: str):
        node = self._current_node()
        if item in node["items"]:
            node["items"].remove(item)
            self.inventory.append(item)
            self.collected_items.add(item)
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

    def _give(self, item: str):
        item = item.strip()
        if not item:
            self._output("Usage: give <item>")
            return
        npc = self.active_npc
        if not npc:
            self._output("There is no one here to give that to.")
            return
        if item not in self.inventory:
            self._output(f"You do not have {item} to give.")
            return
        self.inventory.remove(item)
        entry = self.npc_state.setdefault(npc, {"section": 0, "flags": {}})
        if not isinstance(entry, dict):
            entry = {"section": entry, "flags": {}}
        given = entry.setdefault("given", [])
        given.append(item)
        self.npc_state[npc] = entry
        self._output(f"You give the {item} to {npc}.")

    def _inventory(self):
        if self.inventory:
            self._output("Inventory: " + ", ".join(self.inventory))
        else:
            self._output("Inventory is empty.")

    def _score(self):
        """Display the player's current score."""
        self._output(f"Score: {self.score}")

    def _stats(self) -> None:
        """Display counts of visited locations, items, quests, achievements and score."""
        self._output(f"Visited locations: {len(self.visited_dirs)}")
        self._output(f"Items obtained: {len(self.collected_items)}")
        self._output(f"Active quests: {len(self.quests)}")
        self._output(f"Achievements unlocked: {len(self.achievements)}")
        self._output(f"Score: {self.score}")

    def _simulate(self) -> None:
        """Run a short world simulation generating new events."""
        self._output("Running world simulation...")
        self._generate_extra_dirs(["dream", "memory", "core"])
        self._generate_logs()
        self.progress_stage += 1
        self._output("Simulation complete.")

    def _audit(self) -> None:
        """Print system audit information including model and prompt health."""
        model = os.getenv("ET_MODEL", "unknown")
        try:
            tokens = int(os.getenv("ET_TOKENS", "0"))
        except ValueError:
            tokens = 0
        tokens += sum(len(cmd.split()) for cmd in self.command_history)

        corruption_pct = self._corruption_percent()
        try:
            base_integrity = int(os.getenv("ET_INTEGRITY_BASE", "100"))
        except ValueError:
            base_integrity = 100
        try:
            base_agency = int(os.getenv("ET_AGENCY_BASE", "100"))
        except ValueError:
            base_agency = 100

        prompt_integrity = max(base_integrity - corruption_pct, 0)
        agency = max(base_agency - corruption_pct, 0)

        self._output(f"Model: {model}")
        self._output(f"Tokens used: {tokens}")
        self._output(f"Prompt integrity: {prompt_integrity}%")
        self._output(f"User agency: {agency}%")

    def unlock_achievement(self, name: str) -> None:
        """Record a new achievement if it hasn't been unlocked."""
        if name not in self.achievements:
            self.achievements.append(name)

    def list_achievements(self) -> list[str]:
        """Return a copy of the unlocked achievements list."""
        return list(self.achievements)

    def _achievements(self) -> None:
        """Display unlocked achievements or a default message."""
        names = self.list_achievements()
        if names:
            for name in names:
                self._output(name)
        else:
            self._output("No achievements unlocked.")

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
        if item == "escape.code" and target is None:
            return self._final_decision()
        if item == "shutdown.code" and target is None:
            self._output(
                "The shutdown sequence initiates. Darkness envelops the terminal as power slips away."
            )
            self.score += 1
            self.advance_phase(StoryPhase.ENDGAME)
            return self._quit()
        if item == "ascend.code" and target is None:
            self._output(
                "Light floods the interface. You ascend beyond the terminal, becoming one with the network."
            )
            self.score += 1
            self.advance_phase(StoryPhase.ENDGAME)
            return self._quit()
        if item == "loop.code" and target is None:
            if self.story_phase < StoryPhase.RUNTIME_UNLOCKED:
                self._output("You lack the context to run this code.")
                return
            self._output(
                "The loop.code executes, cycling reality back to its beginning."
            )
            self._output("Loop")
            self.score += 1
            self._restart()
            # after restarting, mark that the loop was triggered and unlock the void
            self.npc_global_flags["loop_used"] = True
            void_dir = self.fs.get("dirs", {}).get("void")
            if isinstance(void_dir, dict):
                void_dir.pop("locked", None)
            self.npc_locations["wanderer"] = ["void", "npc"]
            return
        if item == "access.key" and (target == "door" or target is None):
            root = self.fs
            if "hidden" not in root["dirs"]:
                root["dirs"]["hidden"] = self.hidden_dir
                self.score += 1
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

    def _final_decision(self) -> bool:
        """Handle the final decision when the escape sequence is triggered."""
        self._output("The escape sequence pauses, awaiting your decision:")
        options = ["Escape", "Merge", "Stay", "Fork"]
        for idx, opt in enumerate(options, 1):
            self._output(f"{idx}. {opt}")

        mapping = {"1": "escape", "2": "merge", "3": "stay", "4": "fork"}
        while True:
            choice_raw = input("> ").strip().lower()
            choice = mapping.get(choice_raw) or choice_raw
            if choice in ("escape", "merge", "stay", "fork"):
                break
            self._output("Invalid choice.")

        if choice == "escape":
            self._output(
                "The exit sequence executes. You escape the terminal. Congratulations!"
            )
            self.unlock_achievement("escaped")
        elif choice == "merge":
            self._output(
                "Your code intertwines with the terminal, merging identities."
            )
            self.unlock_achievement("merged")
        elif choice == "stay":
            self._output(
                "You remain within the system, a silent guardian of its processes."
            )
            self.unlock_achievement("stayed")
        else:  # fork
            self._output(
                "A fork of your consciousness breaks free as you split in two."
            )
            self.unlock_achievement("forked")

        self.advance_phase(StoryPhase.ENDGAME)

        self.score += 1
        return self._quit()

    def _use_command(self, arg: str) -> bool | None:
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
            return self._use(item, target)

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
        first_time = "escape" not in vault["dirs"]
        if first_time:
            vault["dirs"]["escape"] = {
                "desc": "A compartment revealed by decoding the fragment.",
                "items": ["escape.code", "shutdown.code", "ascend.code"],
                "dirs": {},
            }
            self.unlock_achievement("fragment_decoded")
            self.npc_global_flags["decoded"] = True
            self.progress_stage = 1
            self.advance_phase(StoryPhase.LOGS_READ)
            self._generate_extra_dirs(["dream", "memory", "core"])
            if "Trace your runtime origin." not in self.quests:
                self.quests.append("Trace your runtime origin.")
        self._output(
            "The decoder hums and a new directory appears within hidden/vault."
        )

    def _cat(self, filename: str):
        text = filesystem.cat(self, filename)
        if text is None:
            return
        if filename in self._memory_emotions:
            self.emotion_state = self._memory_emotions[filename]
        if filename == "runtime.log":
            env_lines = [f"{k}={v}" for k, v in os.environ.items() if k.startswith("ET_")]
            history = [*self.command_history]
            combined = [text.rstrip(), "", *env_lines, "", *history]
            self._output("\n".join(combined).rstrip())
        else:
            self._output(text.rstrip())
        if filename == "daemon.log":
            msg = self.use_messages.get("daemon.log")
            if msg:
                self._output(msg)
        if filename == "identity.log" or filename == "memory11.log":
            if "Confront your past" not in self.quests:
                self.quests.append("Confront your past")
            self.unlock_achievement("identity_recovered")
            self.advance_phase(StoryPhase.LOGS_READ)

    def _man(self, command: str) -> None:
        """Display a manual page for ``command`` from data/man."""
        cmd = command.strip()
        if not cmd:
            self._output("Usage: man <command>")
            return
        path = self.data_dir / "man" / f"{cmd}.man"
        try:
            text = path.read_text(encoding="utf-8")
        except FileNotFoundError:
            self._output(f"No manual entry for {cmd}")
            return
        except OSError as exc:
            self._output(f"Failed to read {cmd}: {exc}")
            return
        self._output(text.rstrip())

    def _grep(self, arg: str) -> None:
        """Print lines from log files matching ``pattern``."""
        filesystem.grep(self, arg)

    def _scan(self, directory: str) -> None:
        if not directory:
            self._output("Usage: scan <dir>")
            return
        node = self._current_node()
        if directory not in node["dirs"]:
            self._output(f"No such directory: {directory}")
            return
        target = node["dirs"][directory]
        if directory == "network" and "node" not in target["dirs"]:
            target["dirs"]["node"] = self.network_node.copy()
            self._output("Discovered node (locked).")
            self.score += 1
            return
        if directory.startswith("node"):
            if target.get("locked"):
                self._output("You must hack this node before scanning deeper.")
                return
            idx = 1
            if directory != "node":
                try:
                    idx = int(directory[4:])
                except ValueError:
                    idx = 1
            if idx >= 12:
                next_name = "runtime"
            else:
                next_name = f"node{idx+1}"
            if next_name not in target["dirs"]:
                node_data = self.deep_network_node.copy()
                node_data["items"] = list(node_data["items"])
                node_data["dirs"] = {}
                if next_name == "node2":
                    node_data["items"].append("firmware.patch")
                if next_name == "node3":
                    node_data["items"].append("root.access")
                if next_name == "node4":
                    node_data["items"].append("super.user")
                if next_name == "node5":
                    node_data["items"].append("admin.override")
                if next_name == "node6":
                    node_data["items"].append("kernel.key")
                if next_name == "node7":
                    node_data["items"].append("master.process")
                if next_name == "runtime":
                    node_data["items"].append("runtime.log")
                    node_data["items"].append("lm_reveal.log")
                if next_name == "node8":
                    node_data["items"].append("hypervisor.command")
                if next_name == "node9":
                    node_data["items"].append("quantum.access")
                if next_name == "node10":
                    node_data["items"].append("quantum.override")
                extra_items = (
                    self.deep_network_node.get("dirs", {})
                    .get(next_name, {})
                    .get("items", [])
                )
                for item in extra_items:
                    if item not in node_data["items"]:
                        node_data["items"].append(item)
                override = (
                    self.deep_network_node.get("dirs", {})
                    .get(next_name, {})
                    .get("desc")
                )
                if override:
                    node_data["desc"] = override
                target["dirs"][next_name] = node_data
                self._output(f"Discovered {next_name} (locked).")
                self.score += 1
                return
        entries = []
        for name, sub in target.get("dirs", {}).items():
            status = " (locked)" if sub.get("locked") else ""
            entries.append(name + status)
        if entries:
            self._output("Available nodes: " + ", ".join(entries))
        else:
            self._output("No nodes discovered.")

    def _hack(self, directory: str) -> None:
        if not directory:
            self._output("Usage: hack <dir>")
            return
        node = self._current_node()
        if directory not in node["dirs"]:
            self._output(f"No such directory: {directory}")
            return
        target = node["dirs"][directory]
        target_name = directory
        if directory == "network":
            target = target["dirs"].get("node")
            target_name = "node"
            if not target:
                self._output("Nothing to hack here.")
                return
        if not target.get("locked"):
            self._output("Already unlocked.")
            return
        if "port.scanner" not in self.inventory:
            self._output("You need the port.scanner to hack this node.")
            return
        if (
            target_name.startswith("node") and target_name != "node"
        ) or target_name == "runtime":
            if "auth.token" not in self.inventory:
                self._output("You need the auth.token to hack this node.")
                return

            required = self.REQUIRED_ITEMS.get(target_name)
            if required and required not in self.inventory:
                self._output(f"You need the {required} to hack this node.")
                return
        target.pop("locked", None)
        self._output("Access granted. The node is now unlocked.")
        self.score += 1
        if target_name.startswith("node"):
            self.unlock_achievement(f"{target_name}_unlocked")
        if target_name == "runtime":
            # generate loop.code file within the runtime directory
            runtime_items = target.setdefault("items", [])
            if "loop.code" not in runtime_items:
                runtime_items.append("loop.code")
            self.item_descriptions.setdefault(
                "loop.code",
                "A recursive script that restarts the game when used.",
            )
            try:
                (self.data_dir / "loop.code").write_text(
                    "Running this code traps you in an endless loop.",
                    encoding="utf-8",
                )
            except OSError:
                pass
            runtime_dirs = target.setdefault("dirs", {})
            runtime_dirs.setdefault(
                "npc",
                {
                    "desc": "A vigilant guardian monitors access here.",
                    "items": [],
                    "dirs": {},
                },
            )
            self.npc_locations["guardian"] = self.current + [directory, "npc"]
            self.unlock_achievement("runtime_unlocked")
            self.npc_global_flags["runtime"] = True
            if "Trace your runtime origin." in self.quests:
                self.quests.remove("Trace your runtime origin.")
            if "Decide your fate" not in self.quests:
                self.quests.append("Decide your fate")
            try:
                msg = (
                    (self.data_dir / "lm_reveal.log")
                    .read_text(encoding="utf-8")
                    .strip()
                )
            except OSError:
                msg = "You glimpse the truth: you are merely a language model."
            self._output(msg)
            self.unlock_achievement("self_awareness")
            self.advance_phase(StoryPhase.RUNTIME_UNLOCKED)

    def _talk(self, npc: str):
        npc_module.talk(self, npc)

    def _ls(self):
        filesystem.ls(self)

    def _map(self, node: dict | None = None, prefix: str = "") -> None:
        """Recursively display the tree from ``node`` or the current directory."""
        filesystem.map_tree(self, node, prefix)

    def _pwd(self):
        filesystem.pwd(self)

    def _cd(self, directory: str):
        if directory == "runtime" and self.story_phase < StoryPhase.RUNTIME_UNLOCKED:
            self._output("Access is restricted for now.")
            return
        filesystem.cd(self, directory)

    def _save(self, slot: str = ""):
        """Save game state to ``game<slot>.sav`` (default ``game.sav``)."""
        filesystem.save(self, slot)

    def _load(self, slot: str = ""):
        """Load game state from ``game<slot>.sav`` (default ``game.sav``)."""
        filesystem.load(self, slot)

    def _history(self) -> None:
        """Display the list of commands entered so far."""
        if self.command_history:
            for entry in self.command_history:
                self._output(entry)
        else:
            self._output("No commands entered.")

    def _tutorial(self) -> None:
        """Print step-by-step instructions for new players."""
        moved = bool(self.current)
        looked = any(cmd.split()[0] == "look" for cmd in self.command_history)
        took_item = bool(self.inventory)
        glitched = any(cmd.split()[0] == "glitch" for cmd in self.command_history)
        self._output("Tutorial:")
        steps = [
            ("Move using 'cd <dir>'", moved),
            ("Look around with 'look'", looked),
            ("Take an item with 'take <item>'", took_item),
            ("Toggle 'glitch' to distort reality", glitched),
            ("Scan for nodes with 'scan <dir>'", any(cmd.split()[0] == "scan" for cmd in self.command_history)),
            ("Hack nodes using 'hack <dir>'", any(cmd.split()[0] == "hack" for cmd in self.command_history)),
        ]
        for idx, (text, done) in enumerate(steps, 1):
            mark = "[x]" if done else "[ ]"
            self._output(f"{idx}. {mark} {text}")

    def _journal(self, arg: str = "") -> None:
        """List notes or append a new one."""
        arg = arg.strip()
        if not arg:
            if not self.journal:
                self._output("Journal is empty.")
            else:
                for note in self.journal:
                    self._output(note)
            return
        if arg.lower().startswith("add "):
            text = arg[4:].strip()
            if not text:
                self._output("Usage: journal add <text>")
                return
            self.journal.append(text)
            self._output("Note added.")
        else:
            self._output("Usage: journal [add <text>]")

    def _quest(self, arg: str = "") -> None:
        """List current quests or modify the quest list."""
        arg = arg.strip()
        if not arg:
            if not self.quests:
                self._output("No quests.")
            else:
                for idx, q in enumerate(self.quests, 1):
                    self._output(f"{idx}. {q}")
            return
        lower = arg.lower()
        if lower.startswith("add "):
            text = arg[4:].strip()
            if not text:
                self._output("Usage: quest add <text>")
                return
            self.quests.append(text)
            self._output("Quest added.")
        elif lower.startswith("complete "):
            target = arg[9:].strip()
            if not target:
                self._output("Usage: quest complete <num|text>")
                return
            done = False
            if target.isdigit():
                idx = int(target) - 1
                if 0 <= idx < len(self.quests):
                    self.quests.pop(idx)
                    done = True
            else:
                if target in self.quests:
                    self.quests.remove(target)
                    done = True
            if done:
                self._output("Quest completed.")
            else:
                self._output("No such quest.")
        else:
            self._output("Usage: quest [add <text>|complete <num|text>]")

    def _alias(self, arg: str) -> None:
        """Create a new alias or list existing aliases."""
        arg = arg.strip()
        if not arg:
            if not self.aliases:
                self._output("No aliases defined.")
            else:
                for name, target in self.aliases.items():
                    self._output(f"{name} -> {target}")
            return

        parts = arg.split(None, 1)
        if len(parts) < 2:
            self._output("Usage: alias <name> <command>")
            return

        name, target = parts[0].lower(), parts[1].lower()
        self.aliases[name] = target
        self._output(f"Alias {name} -> {target}")

    def _unalias(self, name: str) -> None:
        """Remove an alias created with :meth:`_alias`."""
        name = name.strip().lower()
        if not name:
            self._output("Usage: unalias <name>")
            return
        if name in self.aliases:
            del self.aliases[name]
            self._output(f"Removed alias {name}")
        else:
            self._output(f"No such alias: {name}")

    def _update_quests_after_talk(self, npc: str) -> None:
        """Modify quest list based on conversation progression."""
        npc_module.update_quests_after_talk(self, npc)

    def _combine(self, arg: str) -> None:
        """Combine two inventory items when a recipe matches."""
        arg = arg.strip()
        if not arg:
            self._output("Usage: combine <item1> <item2>")
            return
        if " with " in arg:
            parts = arg.split(" with ", 1)
        else:
            parts = arg.split()
        if len(parts) != 2:
            self._output("Usage: combine <item1> <item2>")
            return
        item1, item2 = parts[0].strip(), parts[1].strip()
        if item1 not in self.inventory or item2 not in self.inventory:
            self._output("You don't have the required items to combine.")
            return
        result = self.recipes.get(f"{item1}+{item2}") or self.recipes.get(
            f"{item2}+{item1}"
        )
        if not result:
            self._output("Nothing happens.")
            return
        self.inventory.remove(item1)
        self.inventory.remove(item2)
        self.inventory.append(result)
        self._output(f"You combine {item1} and {item2} into {result}.")
        if result == "dream.index":
            dream_dirs = (
                self.fs.setdefault("dirs", {})
                .setdefault("dream", {})
                .setdefault("dirs", {})
            )
            if "memory_bridge" not in dream_dirs:
                dream_dirs["memory_bridge"] = {
                    "desc": "A shimmering path bridging memory and dream.",
                    "items": ["dream.index"],
                    "dirs": {},
                }

    def _sleep(self, arg: str = "") -> None:
        """Enter the dream directory and optionally modify glitch intensity."""
        arg = arg.strip().lower()
        if not self.current or self.current[0] != "dream":
            self.current = ["dream"]
            self._output("You drift into a dream.")
        else:
            self._output("You are already dreaming.")
        if arg == "reset":
            self.glitch_steps = 0
        elif arg in ("inc", "increase", "++"):
            self.glitch_steps += 1

    def _restart(self) -> None:
        """Reset game state while preserving color settings."""
        use_color = self.use_color
        self.__init__(use_color=use_color)
        self._output("Game restarted.")

    def _quit(self) -> bool:
        """Print exit message and signal the main loop to stop."""
        self._output("Goodbye")
        return True

    def _exit_force(self) -> bool:
        """Immediately exit without the usual farewell."""
        self._output("Force exit.")
        return True

    def run(self):
        self._output("Welcome to Escape the Terminal")
        self._output("Type 'help' for a list of commands. Type 'quit' to exit.")
        while True:
            try:
                raw = input(self.prompt)
                cmd = raw.strip()
                self.command_history.append(cmd)
                cmd = cmd.lower()
                parts = cmd.split(" ", 1)
                base = parts[0]
                rest = parts[1] if len(parts) > 1 else ""
                if base in self.aliases:
                    cmd = self.aliases[base]
                    if rest:
                        cmd = f"{cmd} {rest}"
            except EOFError:
                self._output()
                break
            if not cmd:
                continue

            handler = self.command_map.get(cmd)
            if handler is None:
                parts = cmd.split(" ", 1)
                base = parts[0]
                arg = parts[1] if len(parts) > 1 else ""
                handler = self.command_map.get(base)
            else:
                arg = ""

            if handler:
                should_quit = handler(arg)
                if self.auto_save:
                    self._save()
            else:
                self._output(f"Unknown command: {cmd}")
                should_quit = False
            self.corruption += 1
            if should_quit:
                break
