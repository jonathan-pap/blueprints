# Row filtering

Filter rows early. A `Table.SelectRows` immediately after navigation folds to `WHERE` — the source returns only the rows you need.

## Good

```m
Data = Source{[Schema="dbo", Item="Orders"]}[Data],
#"Filtered" = Table.SelectRows(Data, each [IsActive] = true and [Year] >= 2023),
```

Folds to: `SELECT * FROM dbo.Orders WHERE IsActive = 1 AND Year >= 2023`

## Bad

```m
Data = Source{[Schema="dbo", Item="Orders"]}[Data],
#"AddedColumn" = Table.AddColumn(Data, "Category", each ...),  -- breaks folding
#"Filtered" = Table.SelectRows(#"AddedColumn", each [Year] >= 2023)  -- runs locally
```

Folds to: `SELECT * FROM dbo.Orders`, then the engine pulls all rows, adds the column locally, then filters locally.

## Especially critical for incremental refresh

`RangeStart` / `RangeEnd` filters **must fold** to be effective:

```m
let
    Source = Sql.Database(#"SqlEndpoint", #"Database"),
    Data = Source{[Schema="dbo", Item="Orders"]}[Data],
    #"Filtered" = Table.SelectRows(Data, each
        [OrderDate] >= #"RangeStart" and [OrderDate] < #"RangeEnd")
in
    #"Filtered"
```

If this filter doesn't fold, the incremental refresh defeats its own purpose — every partition pulls all data, then filters in memory.

## See also

- `column-pruning.md` — column reduction (same logic, do early)
- `query-folding.md` — what filter conditions fold vs not
- `../patterns/incremental-refresh.md` — incremental refresh specifics
