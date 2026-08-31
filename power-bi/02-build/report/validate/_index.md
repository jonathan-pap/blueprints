# validate/ — atomic files

- `validate.md` — what to validate when (per page, not per visual) + the cadence table
- `convert-legacy.md` — old `report.json` monolith → PBIR folder layout
- `fix-broken-field-reference.md` — repair visuals that reference a missing field

## Rule

After every mutation in this room, run `validate.md`. If validation fails, do not move on — fix it.
