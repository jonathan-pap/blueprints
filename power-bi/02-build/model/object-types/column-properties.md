# Column properties (DataColumn + CalculatedColumn)

## Required

- `dataType` — `string`, `int64`, `double`, `decimal`, `dateTime`, `boolean`, `binary`, `unknown`, `variant`, `automatic`
- `sourceColumn` (DataColumn only) — must match M output exactly
- `expression` (CalculatedColumn only) — DAX
- `lineageTag` — unique GUID

## Aggregation

- `summarizeBy` — `default`, `none`, `sum`, `min`, `max`, `count`, `average`, `distinctCount`

### Pitfall — `summarizeBy: none` silently breaks Sum/Avg in visuals

A numeric column declared with `summarizeBy: none` + `annotation SummarizationSetBy = Automatic` renders nothing when bound to a chart that needs Sum or Avg — the chart shows categories with empty values and no error. Count (`Aggregation.Function: 2`) still works because it ignores `summarizeBy`, so the symptom reads as "sum of `<col>` missing" while counts/donuts look fine on the same field.

Some external generators (e.g. `powerbi-lineage`) emit every numeric column with this pair. Fix in TMDL:

```tmdl
column 'Trade Value'
    dataType: double
    summarizeBy: sum                       ← was `none`
    sourceColumn: TradeValue

    annotation SummarizationSetBy = User   ← was `Automatic`; User stops Desktop reverting
```

`User` stops Desktop's SummarizationSetBy heuristic from reverting the edit to `none` on next save. Re-running the external generator re-emits the bad pair, so reapply after each regeneration.

## Type variant

- `type` — `data`, `calculated`, `rowNumber`, `calculatedTableColumn`

## Visibility / metadata

- `isHidden` (flag)
- `isKey` (flag) — marks as table key
- `isNullable` (flag)
- `isUnique` (flag)
- `isNameInferred` (flag) — name inferred from source
- `isDefaultLabel` (flag)
- `isDefaultImage` (flag)
- `isDataTypeInferred` (flag)
- `isAvailableInMdx` (flag)
- `keepUniqueRows` (flag)

## Display

- `displayFolder: 'folder\nested'` — use `\` for nesting
- `formatString: '#,##0'`
- `alignment` — `default`, `left`, `right`, `center`
- `encodingHint` — `default`, `hash`, `value`

## Sorting

- `sortByColumn: ColumnName` — sort this column by another (e.g. `Month Name` sorted by `Month Number`)

## See also

- `../fix-pattern/summarize-by-key.md`
- `../fix-pattern/format-string-by-type.md`
- `../fix-pattern/pbi-format-hint-readded.md`
