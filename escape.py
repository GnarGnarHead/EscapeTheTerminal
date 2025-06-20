"""Escape the Terminal - basic shell-like game."""


FILESYSTEM = {
    "readme.txt": (
        "You awaken in a strange shell. Type 'help' for commands."
    ),
    "home": {
        "note.txt": "The system feels old, but something watches..."
    },
    "logs": {
        "boot.log": "[BOOT] System initialized."
    },
}


def get_node(path):
    node = FILESYSTEM
    for part in path:
        if isinstance(node, dict) and part in node:
            node = node[part]
        else:
            return None
    return node


def main():
    print("Welcome to Escape the Terminal")
    print("Type 'help' for a list of commands. Type 'quit' to exit.")
    cwd = []
    while True:
        try:
            cmd = input("/" + "/".join(cwd) + "> ").strip()
        except EOFError:
            print()
            break
        if not cmd:
            continue
        args = cmd.split()
        if args[0] == "help":
            print("Commands: help, quit, ls, cd <dir>, cat <file>")
        elif args[0] in ("quit", "exit"):
            print("Goodbye")
            break
        elif args[0] == "ls":
            node = get_node(cwd)
            if isinstance(node, dict):
                print("\n".join(sorted(node.keys())))
            else:
                print("Not a directory")
        elif args[0] == "cd":
            if len(args) < 2:
                print("Usage: cd <directory>")
                continue
            target = args[1]
            if target == "..":
                if cwd:
                    cwd.pop()
                continue
            node = get_node(cwd + [target])
            if isinstance(node, dict):
                cwd.append(target)
            else:
                print(f"No such directory: {target}")
        elif args[0] == "cat":
            if len(args) < 2:
                print("Usage: cat <file>")
                continue
            node = get_node(cwd + [args[1]])
            if isinstance(node, str):
                print(node)
            else:
                print(f"No such file: {args[1]}")
        else:
            print(f"Unknown command: {cmd}")


if __name__ == "__main__":
    main()
