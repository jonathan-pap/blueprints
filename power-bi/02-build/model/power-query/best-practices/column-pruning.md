# Column pruning

Remove columns as early as possible. Every column not removed travels through every subsequent step — and folds to a wider SQL SELECT.

## Good

```m
-- Remove columns immediately after navigation
Data = Source{[Schema="dbo", Item="Orders"]}[Data],
#"Selected" = Table.SelectColumns(Data, {"OrderId", "Date", "Amount"}),
-- ... subsequent steps process only 3 columns
```

Folds to: `SELECT OrderId, Date, Amount FROM dbo.Orders ...`

## Bad

```m
-- Remove columns at the end after all transforms
Data = Source{[Schema="dbo", Item="Orders"]}[Data],
#"Filtered" = Table.SelectRows(Data, each [Status] <> "Cancelled"),
#"Typed" = Table.TransformColumnTypes(#"Filtered", {{...}}),
-- ... all 47 columns flow through every step
#"Final" = Table.RemoveColumns(#"Typed", {"Col1", "Col2", "Col3", ..."Col44"})
```

Folds to: `SELECT * FROM dbo.Orders WHERE Status <> 'Cancelled'`, then locally drops the columns. Wasted bandwidth.

## Why it matters

- Reduced data transfer from source
- Smaller intermediate tables in memory
- Faster downstream steps
- Better dictionary compression when types are applied to selected columns only

## See also

- `query-folding.md` — `Table.SelectColumns` is one of the cleanest-folding operations
- `../safe-pattern.md` — full order: filter → select → type → sort → custom
- `row-filtering.md` — apply filters BEFORE selecting columns where possible
