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

