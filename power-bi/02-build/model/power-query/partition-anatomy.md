# Partition expression anatomy

Each import table in a semantic model has a partition with an M expression defining what data gets loaded during refresh. The expression typically connects to a data source, navigates to a table/view, applies transformations.

## Structure

```m
let
    Source = Sql.Database(#"SqlEndpoint", #"Database"),
    Data = Source{[Schema="dbo", Item="Orders"]}[Data],
    #"Removed Columns" = Table.RemoveColumns(Data, {"InternalId"}),
    #"Changed Type" = Table.TransformColumnTypes(#"Removed Columns", {{"Amount", Currency.Type}})
in
    #"Changed Type"
```

## Key elements

- **Parameters** — `#"SqlEndpoint"`, `#"Database"` are shared M parameters defined at the model level (in `expressions.tmdl`).
- **Navigation** — `Source{[Schema="dbo", Item="Orders"]}[Data]` navigates to a specific table.
- **Steps** — each step is a named variable in the `let...in` chain.
- **Quoted identifiers** — step names with spaces use `#"Step Name"` syntax.

## In TMDL

The partition lives inside the table's TMDL file:

```tmdl
table 'Sales'
    column 'OrderID'
        dataType: int64
        sourceColumn: OrderID

    partition 'Sales-Partition' = m
        mode: import
        source = ```
                let
                    Source = Sql.Database(#"SqlEndpoint", #"Database"),
                    Data = Source{[Schema="dbo", Item="Orders"]}[Data]
                in
                    Data
                ```
```

`= m` declares it's an M partition. `mode: import` declares it as Import-mode (vs DirectQuery, DirectLake).

## See also

- `extract-expressions.md` — pulling partitions from deployed models
- `safe-pattern.md` — recommended order of M steps
- `../../object-types/partition-properties.md` — full partition property reference
