"""Escape the Terminal - minimal command loop"""


def main():
    print("Welcome to Escape the Terminal")
    print("Type 'help' for a list of commands. Type 'quit' to exit.")
    location_description = (
        "You find yourself in a dimly lit terminal session. The prompt blinks patiently."
    )
    room_items = ["access.key"]
    inventory = []
    while True:
        try:
            cmd = input('> ').strip().lower()
        except EOFError:
            print()
            break
        if cmd == 'help':
            print("Available commands: help, look, take <item>, inventory, quit")
        elif cmd == 'look':
            print(location_description)
            if room_items:
                print("You see: " + ", ".join(room_items))
        elif cmd.startswith('take '):
            item = cmd.split(' ', 1)[1]
            if item in room_items:
                room_items.remove(item)
                inventory.append(item)
                print(f"You pick up the {item}.")
            else:
                print(f"There is no {item} here.")
        elif cmd == 'inventory':
            if inventory:
                print("Inventory: " + ", ".join(inventory))
            else:
                print("Inventory is empty.")
        elif cmd in ('quit', 'exit'):
            print("Goodbye")
            break
        elif not cmd:
            continue
        else:
            print(f"Unknown command: {cmd}")


if __name__ == '__main__':
    main()
