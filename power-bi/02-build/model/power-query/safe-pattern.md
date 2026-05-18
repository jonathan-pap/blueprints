# Safe pattern for writing M

Order M steps to maximize query folding. The rule: **do all foldable work first, then non-foldable work.**

## Template

```m
let
    Source = Sql.Database(SqlEndpoint, Database),
    Data = Source{[Schema="dbo", Item="MyTable"]}[Data],

    -- 1. Filter rows (folds to WHERE)
    Filtered = Table.SelectRows(Data, each [IsActive] = true),

    -- 2. Select columns (folds to SELECT)
    Selected = Table.SelectColumns(Filtered, {"Id", "Date", "Amount"}),

    -- 3. Set types (folds to CAST)
    Typed = Table.TransformColumnTypes(Selected, {{"Amount", Currency.Type}}),

    -- 4. Sort if needed (folds to ORDER BY)
    Sorted = Table.Sort(Typed, {{"Date", Order.Descending}}),

    -- 5. Non-foldable transforms LAST
    Added = Table.AddColumn(Sorted, "Category", each if [Amount] > 1000 then "High" else "Low")
in
    Added
```

## Why this order

- Filter early → less data flowing through subsequent steps
- Select early → fewer columns to compress / type / transform
- Type early → casts fold to SQL CAST
- Custom logic last → once `Table.AddColumn` with `each` breaks folding, every subsequent step runs locally; put it at the end so the rest still folds

## If logic is too complex for M

Use `Value.NativeQuery` to pass native SQL:

```m
let
    Source = Sql.Database(SqlEndpoint, Database),
    Data = Value.NativeQuery(Source,
        "SELECT Id, Date, Amount FROM dbo.MyTable WHERE IsActive = 1",
        null, [EnableFolding=true])
in
    Data
```

`EnableFolding=true` allows subsequent M steps to fold on top of the native query result.

## See also

- `best-practices/query-folding.md` — what folds, what doesn't, why it matters
- `patterns/native-query.md` — when to use Value.NativeQuery
