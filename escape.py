"""Escape the Terminal - minimal command loop.

This module now exposes a :class:`Game` object to make future expansion
easier while preserving the original command-line interface.
"""


class Game:
    """Simple command dispatcher for the terminal adventure."""

    def __init__(self):
        self.inventory = []
        self.fs = {
            "desc": (
                "You find yourself in a dimly lit terminal session. "
                "The prompt blinks patiently."
            ),
            "items": ["access.key"],
            "dirs": {
                "hidden": {
                    "desc": "A directory shrouded in mystery.",
                    "items": ["treasure.txt"],
                    "dirs": {},
                }
            },
        }
        self.current = []  # path as list of directory names
        self.item_descriptions = {
            "access.key": "A slim digital token rumored to unlock hidden directories.",
            "treasure.txt": "A file filled with untold riches.",
        }
        self.use_messages = {
            "access.key": "The key hums softly and a hidden directory flickers into view."
        }
        self.save_file = "game.sav"

    def _print_help(self):
        print(
            "Available commands: help, look, ls, cd <dir>, take <item>, drop <item>, "
            "inventory, examine <item>, use <item>, save, load, quit"
        )

    def _current_node(self):
        node = self.fs
        for part in self.current:
            node = node["dirs"][part]
        return node

    def _look(self):
        node = self._current_node()
        print(node["desc"])
        entries = [d + "/" for d in node["dirs"]] + list(node["items"])
        if entries:
            print("You see: " + ", ".join(entries))

    def _take(self, item: str):
        node = self._current_node()
        if item in node["items"]:
            node["items"].remove(item)
            self.inventory.append(item)
            print(f"You pick up the {item}.")
        else:
            print(f"There is no {item} here.")

    def _drop(self, item: str):
        if item in self.inventory:
            self.inventory.remove(item)
            node = self._current_node()
            node["items"].append(item)
            print(f"You drop the {item}.")
        else:
            print(f"You do not have {item} to drop.")

    def _inventory(self):
        if self.inventory:
            print("Inventory: " + ", ".join(self.inventory))
        else:
            print("Inventory is empty.")

    def _examine(self, item: str):
        node = self._current_node()
        if item in self.inventory or item in node["items"]:
            desc = self.item_descriptions.get(item, "It's unremarkable.")
            print(desc)
        else:
            print(f"You do not have {item} to examine.")

    def _use(self, item: str):
        if item not in self.inventory:
            print(f"You do not have {item} to use.")
            return
        msg = self.use_messages.get(item)
        if msg:
            print(msg)
        else:
            print(f"You can't use {item} right now.")

    def _ls(self):
        node = self._current_node()
        entries = [d + '/' for d in node['dirs']] + list(node['items'])
        if entries:
            print(" ".join(entries))
        else:
            print("Nothing here.")

    def _cd(self, directory: str):
        if directory in ('.', ''):
            return
        if directory == '..':
            if self.current:
                self.current.pop()
            else:
                print("Already at root.")
            return
        node = self._current_node()
        if directory in node['dirs']:
            self.current.append(directory)
        else:
            print(f"No such directory: {directory}")

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
            print(f"Failed to save: {e}")
        else:
            print("Game saved.")

    def _load(self):
        import json

        try:
            with open(self.save_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            print("No save file found.")
            return
        except OSError as e:
            print(f"Failed to load: {e}")
            return
        self.fs = data.get("fs", self.fs)
        self.inventory = data.get("inventory", [])
        self.current = data.get("current", [])
        print("Game loaded.")

    def run(self):
        print("Welcome to Escape the Terminal")
        print("Type 'help' for a list of commands. Type 'quit' to exit.")
        while True:
            try:
                cmd = input('> ').strip().lower()
            except EOFError:
                print()
                break
            if cmd in ('help', 'h'):
                self._print_help()
            elif cmd in ('look', 'look around'):
                self._look()
            elif cmd == 'ls':
                self._ls()
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
                item = cmd.split(' ', 1)[1]
                self._use(item)
            elif cmd == 'save':
                self._save()
            elif cmd == 'load':
                self._load()
            elif cmd in ('quit', 'exit'):
                print("Goodbye")
                break
            elif not cmd:
                continue
            else:
                print(f"Unknown command: {cmd}")


def main():
    Game().run()


if __name__ == '__main__':
    main()
