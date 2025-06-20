import os


def main():
    print("Escape the Terminal - prototype")
    print("Type 'help' for commands.")
    fs = {
        "dream": {"start.log": "A cryptic dream sequence..."},
        "memory": {"fragment.txt": "Faded memories stir."},
        "core": {"system.txt": "Core diagnostics corrupted."},
        "logs": {"boot.log": "Incomplete boot sequence detected."},
        "README.txt": "You awaken in a blank console."
    }
    cwd = []  # path list

    def get_dir(path):
        d = fs
        for p in path:
            d = d.get(p)
            if not isinstance(d, dict):
                return None
        return d

    while True:
        path = '/' + '/'.join(cwd)
        command = input(f"{path or '/'}> ").strip()
        if not command:
            continue
        if command in ("exit", "quit"):
            print("Exiting.")
            break
        if command == "help":
            print("Available commands: ls, cd <dir>, cat <file>, help, exit")
            continue
        if command == "ls":
            d = get_dir(cwd)
            if d is None:
                print("Error: invalid directory")
            else:
                print("  ".join(d.keys()))
            continue
        if command.startswith("cd "):
            target = command[3:].strip()
            if target == "..":
                if cwd:
                    cwd.pop()
                continue
            d = get_dir(cwd)
            if d and target in d and isinstance(d[target], dict):
                cwd.append(target)
            else:
                print(f"No such directory: {target}")
            continue
        if command.startswith("cat "):
            file = command[4:].strip()
            d = get_dir(cwd)
            if d and file in d and isinstance(d[file], str):
                print(d[file])
            else:
                print(f"No such file: {file}")
            continue
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
