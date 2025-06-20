"""Escape the Terminal - minimal command loop.

This module now exposes a :class:`Game` object to make future expansion
easier while preserving the original command-line interface.
"""


class Game:
    """Simple command dispatcher for the terminal adventure."""

    def __init__(self):
        self.location_description = (
            "You find yourself in a dimly lit terminal session. "
            "The prompt blinks patiently."
        )
        self.room_items = ["access.key"]
        self.inventory = []
        self.item_descriptions = {
            "access.key": "A slim digital token rumored to unlock hidden directories."
        }

    def _print_help(self):
        print(
            "Available commands: help, look, take <item>, inventory, "
            "examine <item>, quit"
        )

    def _look(self):
        print(self.location_description)
        if self.room_items:
            print("You see: " + ", ".join(self.room_items))

    def _take(self, item: str):
        if item in self.room_items:
            self.room_items.remove(item)
            self.inventory.append(item)
            print(f"You pick up the {item}.")
        else:
            print(f"There is no {item} here.")

    def _inventory(self):
        if self.inventory:
            print("Inventory: " + ", ".join(self.inventory))
        else:
            print("Inventory is empty.")

    def _examine(self, item: str):
        if item in self.inventory or item in self.room_items:
            desc = self.item_descriptions.get(item, "It's unremarkable.")
            print(desc)
        else:
            print(f"You do not have {item} to examine.")

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
            elif cmd.startswith('take '):
                item = cmd.split(' ', 1)[1]
                self._take(item)
            elif cmd in ('inventory', 'inv', 'i'):
                self._inventory()
            elif cmd.startswith('examine '):
                item = cmd.split(' ', 1)[1]
                self._examine(item)
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
