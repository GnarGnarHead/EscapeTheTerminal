# Story Phase Progression

The narrative in **Escape the Terminal** advances through a handful of phases
tracked by `Game.story_phase`.  Each phase unlocks new areas or dialog and can
be checked by commands or NPC interactions.

## Phases

1. `INTRO` – Initial state at game start.
2. `LOGS_READ` – Set when key logs such as `identity.log` or the memory
   fragment are read and decoded.
3. `RUNTIME_UNLOCKED` – Achieved after hacking the `runtime` node.
4. `ENDGAME` – Reached once any of the end sequences execute.

The helper `Game.advance_phase()` moves the current phase forward if the new
value is greater than the existing one.

## Usage

Command handlers and NPC dialogs may check `game.story_phase` to restrict
access. For example the guardian NPC only speaks after the runtime has been
unlocked and the loop code cannot run beforehand.  Directories like `void/`
are likewise inaccessible until the appropriate phase.
