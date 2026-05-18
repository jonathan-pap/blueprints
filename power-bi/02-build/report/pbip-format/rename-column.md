# Rename a column (cascade)

Renaming a column `'Table'[OldCol]` → `'Table'[NewCol]`. Less invasive than a table rename but still cross-cutting.

## Files to update

1. `<name>.SemanticModel/definition/tables/<table>.tmdl` — the `column 'OldCol'` declaration.
2. Inside the table TMDL: any `sortByColumn: OldCol` references.
3. `<name>.SemanticModel/definition/cultures/*.tmdl` — translations.
4. `<name>.SemanticModel/definition/perspectives/*.tmdl` — perspective membership.
5. **All** `<name>.Report/definition/pages/<page>/visuals/<visual>/visual.json` — every `Property: "OldCol"` and DAX referencing `'Table'[OldCol]`.
6. `<name>.Report/definition/reportExtensions.json` — thin-report measures using the column.
7. `<name>.SemanticModel/DAXQueries/*.dax` and `<name>.Report/DAXQueries/*.dax`.

## Procedure

```bash
PROJ="<project>"
TABLE="Sales"
OLD="OldCol"
NEW="NewCol"

# 1. Grep
grep -rln "'$TABLE'\[$OLD\]\|Property\": \"$OLD\"" "$PROJ.Report/" "$PROJ.SemanticModel/"

# 2. Edit the TMDL declaration in <table>.tmdl
# 3. Sed the rest
grep -rl "'$TABLE'\[$OLD\]\|Property\": \"$OLD\"" "$PROJ.Report/" "$PROJ.SemanticModel/" | \
  xargs sed -i "s/'$TABLE'\[$OLD\]/'$TABLE'\[$NEW\]/g; s/Property\": \"$OLD\"/Property\": \"$NEW\"/g"

# 4. Validate
pbir validate "$PROJ.Report"
```

## Verify

`post-rename-checklist.md`.

## Gotcha

`sortByColumn` references the bare column name (no table prefix). The sed above misses those — handle separately:

```bash
grep -rn "sortByColumn: $OLD" "$PROJ.SemanticModel/"
```
