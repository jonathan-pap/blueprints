# Update a property (TMDL)

Change one property on one object. Edit the relevant `.tmdl` file in place.

## Procedure

1. Find the file:

```bash
grep -rln "measure 'Total Revenue'" "<project>.SemanticModel/definition/"
```

2. Edit the property at depth 2 (column/measure properties live one level deeper than the declaration):

```tmdl
measure 'Total Revenue' = SUM('Sales'[Amount])
    formatString: #,##0.00        ← change here
    displayFolder: 1. Revenue
    lineageTag: abc-123           ← never modify
```

3. Validate:

```bash
bash ../../../04-review/hooks/validate-tmdl.sh "<project>.SemanticModel"
```

## What you can change safely

- `formatString`, `formatStringDefinition`
- `displayFolder`
- `description` (also settable via `///` line above the declaration)
- `isHidden`
- `summarizeBy` (column only)
- `dataType` (with caution — may require source change)
- `sortByColumn` (column only)

## What never to change

- `lineageTag` — these are identifiers; tools track objects by GUID.
- `PBI_FormatHint` annotations — Desktop re-adds them; let them be.

## See also

- `measure-expression.md` — change the DAX, not a property
- `../fix-pattern/_index.md` — common property bugs
- `../object-types/_index.md` — valid values for each property
