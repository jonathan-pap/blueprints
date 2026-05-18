# Rename a table (cascade)

Renaming `'OldTable'` → `'NewTable'` touches more files than a measure rename because every column and measure of the table is referenced as `'Table'[Field]`.

## Files to update

1. **Rename the TMDL file**: `<name>.SemanticModel/definition/tables/OldTable.tmdl` → `NewTable.tmdl`.
2. Inside the file: `table 'OldTable'` → `table 'NewTable'`.
3. `<name>.SemanticModel/definition/relationships.tmdl` — every `fromTable: 'OldTable'` / `toTable: 'OldTable'`.
4. `<name>.SemanticModel/definition/model.tmdl` — `ref table 'OldTable'` entries.
5. `<name>.SemanticModel/definition/cultures/*.tmdl` — translations for the table.
6. `<name>.SemanticModel/definition/perspectives/*.tmdl` — perspective membership.
7. **All** `<name>.Report/definition/pages/<page>/visuals/<visual>/visual.json` — every `Entity: "OldTable"` and DAX referencing `'OldTable'[Field]`.
8. `<name>.Report/definition/reportExtensions.json` — thin-report measures using the table.
9. `<name>.SemanticModel/DAXQueries/*.dax` and `<name>.Report/DAXQueries/*.dax` — saved DAX queries.

## Procedure

```bash
PROJ="<project>"
OLD="OldTable"
NEW="NewTable"

# 1. Grep to find every reference
grep -rln "'$OLD'" "$PROJ.Report/" "$PROJ.SemanticModel/"
grep -rln "Entity\": \"$OLD\"" "$PROJ.Report/"

# 2. Rename the TMDL file
mv "$PROJ.SemanticModel/definition/tables/$OLD.tmdl" "$PROJ.SemanticModel/definition/tables/$NEW.tmdl"

# 3. Sed across everything
grep -rl "'$OLD'\|Entity\": \"$OLD\"" "$PROJ.Report/" "$PROJ.SemanticModel/" | \
  xargs sed -i "s/'$OLD'/'$NEW'/g; s/Entity\": \"$OLD\"/Entity\": \"$NEW\"/g"

# 4. Validate
pbir validate "$PROJ.Report"
bash ../../../04-review/hooks/validate-tmdl.sh "$PROJ.SemanticModel"
```

## Verify

`post-rename-checklist.md`.

## Gotcha

`SparklineData` selectors embed Entity references in compact strings. Grep catches them; structured JSON walkers may miss them.
