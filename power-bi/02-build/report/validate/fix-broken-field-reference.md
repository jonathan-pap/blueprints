# Fix a broken field reference

Visual references a field that no longer exists in the model (deleted, renamed, or model swap). PBI Desktop shows a broken-visual badge.

## Find

```bash
pbir validate "<project>.Report"                       # lists broken refs
pbir fields find "<project>.Report" -f "Sales.OldName" # specific
```

## Decide

- **Renamed** in the model → rebind to the new name. Use `../bind/swap-field.md`.
- **Deleted** from the model → either remove the binding (`../bind/clear-binding.md`) or remove the visual.
- **Typo all along** → fix in the visual JSON (one-line edit) and re-validate.

## Cascade renames

If the rename was a deliberate model-side rename, the report side needs the full cascade — see `../pbip-format/rename-measure.md` (or `rename-column.md` / `rename-table.md`) which lists every file location to update at once.

## After

`validate.md`. Reopen in Desktop to confirm the broken badge is gone.
