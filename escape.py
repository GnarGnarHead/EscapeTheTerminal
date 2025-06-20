"""Escape the Terminal - minimal command loop"""


def main():
    print("Welcome to Escape the Terminal")
    print("Type 'help' for a list of commands. Type 'quit' to exit.")
    location_description = "You find yourself in a dimly lit terminal session. The prompt blinks patiently."
    while True:
        try:
            cmd = input('> ').strip().lower()
        except EOFError:
            print()
            break
        if cmd == 'help':
            print("Available commands: help, look, quit")
        elif cmd == 'look':
            print(location_description)
        elif cmd in ('quit', 'exit'):
            print("Goodbye")
            break
        elif not cmd:
            continue
        else:
            print(f"Unknown command: {cmd}")


if __name__ == '__main__':
    main()
