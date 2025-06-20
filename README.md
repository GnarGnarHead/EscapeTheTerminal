# EscapeTheTerminal
A retro cybertext adventure inspired by Philip K. Dick and William Gibson.

This project is a minimalist terminal game. For the long-term vision, see [VISIONDOCUMENT.md](VISIONDOCUMENT.md).

## Setup
1. Install Python 3.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the game:
   ```bash
   python escape.py
   ```
   Use `help` inside the game for available commands and `quit` to exit.

### Basic Commands
- `ls` – list files in the current directory
- `cd <dir>` – change directory (`..` to go up)
- `cat <file>` – view file contents

## Running Tests
Tests require `pytest` and can be executed with:
```bash
pytest
```
