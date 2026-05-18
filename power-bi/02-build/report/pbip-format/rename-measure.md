# Rename a measure (cascade)

Renaming `[Old Name]` → `[New Name]` requires touching every reference. Miss one → broken visual or DAX error.

## Files to update

1. `<name>.SemanticModel/definition/tables/<table>.tmdl` — the `measure` declaration itself.
2. `<name>.SemanticModel/definition/cultures/<locale>.tmdl` — translations (if any).
3. `<name>.Report/definition/pages/<page>/visuals/<visual>/visual.json` — field bindings, conditional formatting expressions, titles using the measure.
4. `<name>.Report/definition/reportExtensions.json` — thin-report measures referencing it.
5. `<name>.SemanticModel/DAXQueries/*.dax` — saved model queries.
6. `<name>.Report/DAXQueries/*.dax` — saved report queries.

## Procedure

```bash
# 1. Grep first to find all references
grep -rln "\[Old Name\]" "<project>.Report/" "<project>.SemanticModel/"

# 2. Edit TMDL declaration in tables/<table>.tmdl
# 3. Sed across the rest (preview without -i first)
grep -rl "\[Old Name\]" "<project>.Report/" "<project>.SemanticModel/" | \
  xargs sed -i 's/\[Old Name\]/\[New Name\]/g'

# 4. Validate
pbir validate "<project>.Report"
```

## Verify after

Run `post-rename-checklist.md`.

## Gotcha

`SparklineData` selectors embed Entity references in compact strings that don't follow the standard `SourceRef.Entity` JSON shape. Plain grep catches them, structured JSON walkers may miss them.
