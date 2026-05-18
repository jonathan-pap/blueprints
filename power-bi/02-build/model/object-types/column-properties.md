# Column properties (DataColumn + CalculatedColumn)

## Required

- `dataType` — `string`, `int64`, `double`, `decimal`, `dateTime`, `boolean`, `binary`, `unknown`, `variant`, `automatic`
- `sourceColumn` (DataColumn only) — must match M output exactly
- `expression` (CalculatedColumn only) — DAX
- `lineageTag` — unique GUID

## Aggregation

- `summarizeBy` — `default`, `none`, `sum`, `min`, `max`, `count`, `average`, `distinctCount`

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
