# Game Mechanics

This file explains optional mechanics beyond the basic exploration commands.

## Score Tracking
Certain actions such as discovering network nodes or escaping the terminal
increase the player's score. Use the `score` command at any time to display the
current value.

Example:

```text
> score
Score: 0
```

## Stats Overview
Use the `stats` command to review your progress. It prints how many locations
you have visited, how many items you've collected and your current score.

```text
> stats
Visited locations: 1
Items obtained: 0
Score: 0
```

## Restarting
The `restart` command resets the game world and inventory while keeping any
current color settings. It is useful for quickly starting over without leaving
the program.

```text
> restart
Game restarted.
```

## Achievements
Persistent achievements are stored inside `Game.achievements`. They are saved
alongside other game data and can be listed with the `achievements` command.

## Journal Notes
The `journal` command lets you keep simple notes. Without arguments it prints
any saved lines. Use `journal add <text>` to append a new entry.

```text
> journal add Met the archivist in the vault
Note added.
> journal
Met the archivist in the vault
```

## Quests
Quests help track ongoing objectives. Run `quest` to list them, `quest add <text>`
to create one and `quest complete <num|text>` to mark it finished.

```text
> quest add Find the hidden key
Quest added.
> quest
1. Recover your lost memory
2. Find the hidden key
> quest complete 2
Quest completed.
```

## Mood Changes
Reading certain memory logs updates the avatar's emotional state. When the mood
changes a short line like `(You feel alarmed.)` is shown before the next
message.

```text
> cat memory8.log
(You feel alarmed.)
...log contents...
```

