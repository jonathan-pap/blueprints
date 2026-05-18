# Post-rename verification

Run after any cascade rename (table / measure / column). Same content as `../../02-build/report/pbip-format/post-rename-checklist.md` — duplicated here for review-time convenience.

## Commands

```bash
PROJ="<project>"
OLD="\[Old Name\]"   # or 'Old Table' or [Old Column]

# 1. Zero matches of old name anywhere
grep -rn "$OLD" "$PROJ.Report/" "$PROJ.SemanticModel/"

# 2. PBIR validates clean
pbir validate "$PROJ.Report"

# 3. TMDL validates clean
bash ../hooks/validate-tmdl.sh "$PROJ.SemanticModel"

# 4. Both DAXQueries directories checked
grep -rn "$OLD" "$PROJ.SemanticModel/DAXQueries/" "$PROJ.Report/DAXQueries/"

# 5. Full project validator
python ../scripts/validate_pbip.py "$PROJ"
```

If any step returns hits, the rename is incomplete — open each match and fix.

## Then reopen in Desktop

Confirm no broken-visual badges, no measure-not-found errors.

## Common misses

- `SparklineData` selectors embed Entity refs in compact strings — easy for structured walkers to miss, grep catches them.
- DAX query files in TWO locations: `<name>.SemanticModel/DAXQueries/` AND `<name>.Report/DAXQueries/`.
- `sortByColumn` references the bare column name (no table prefix) — separate grep needed.
- Cultures: `<locale>.tmdl` files have separate translations of the renamed object.
