# Add a column (DataColumn, TMDL)

A regular column sourced from a Power Query partition. Place inside the `table` block at depth 1.

## Pattern

```tmdl
column 'Order Date'
    dataType: dateTime
    isNullable
    displayFolder: 1. Dates
    lineageTag: <generate-new-guid>
    summarizeBy: none
    sourceColumn: Order Date

    annotation SummarizationSetBy = Automatic
```

## Required vs optional

- `dataType` — required for data columns.
- `sourceColumn` — required. Must match the column name in the partition's M output exactly.
- `lineageTag` — required (unique GUID for new columns).
- `summarizeBy` — recommended. `none` for keys / attributes / dates / flags; `sum` for additive numeric facts; `none` for rates / percentages.
- `displayFolder` — optional. Use `\` for nesting (`1. Year\Quarter`).
- `isHidden` — bare keyword flag (no value), include the line for hidden columns.

## Boolean flags

Write the keyword alone on its own line — no value:

```tmdl
column 'CustomerID'
    dataType: int64
    isHidden
    isKey
    lineageTag: <guid>
    summarizeBy: none
    sourceColumn: CustomerID
```

## After

`bash ../../../04-review/hooks/validate-tmdl.sh "<project>.SemanticModel"` then reopen Power BI Desktop.

## See also

- `calculated-column.md` — column computed by DAX (different shape)
- `../fix-pattern/summarize-by-key.md` — fix `summarizeBy: sum` on key columns
- `../object-types/column-properties.md` — full property reference
