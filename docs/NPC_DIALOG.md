# NPC Dialog Files

The `.dialog` format drives conversations with NPCs. Each file is processed line by line and may be split into multiple **sections** separated by a line containing only `---`. Talking to an NPC advances to the next section on each interaction while keeping any flags that were set previously.

## Choices
Lines beginning with `>` are presented to the player as numbered options. The selected text is echoed back and may set a flag:

```
> Ask about escape [+curious]
> Demand access [-polite]
> Pick a style [style=quiet]
```

- `+flag` sets `flag` to `true`.
- `-flag` sets `flag` to `false`.
- `flag` without a prefix also sets the flag to `true`.
- `flag=value` stores an arbitrary value.

## Conditional lines
Lines starting with `?` show text only when a flag condition is met. Prefix the flag with `!` to invert the check.

```
?curious:The NPC nods at your enthusiasm.
?!curious:The NPC looks skeptical.
```

## Sections
Use `---` to divide the dialog into sections. On the first conversation the first section is displayed. Subsequent talks continue with the next section until the end of the file is reached.

## Registering NPCs
Each NPC name must be mapped to its directory within `Game.npc_locations`. For example:

```python
from escape import Game

Game.npc_locations['merchant'] = ['market', 'npc']
```

This places a new `merchant.dialog` under `data/npc/` and associates it with the `market/npc/` location.

## Validator script
A small helper lives at `escape/utils/validate_dialog.py` to check dialog files for common mistakes. Run it with Python and pass one or more files or directories or use the `validate-dialog` command installed with the game:

```bash
validate-dialog escape/data/npc
```

```bash
python -m escape.utils.validate_dialog escape/data/npc
```

The script reports missing `:` in conditional lines and unclosed `[]` markers in choices. It exits with a non-zero status when any problems are found.
