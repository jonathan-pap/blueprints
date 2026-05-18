# Add a table sourced from M (TMDL)

Create `<project>.SemanticModel/definition/tables/<Name>.tmdl` and register it in `model.tmdl`.

## File: `tables/Sales.tmdl`

```tmdl
table 'Sales'
    lineageTag: <generate-new-guid>

    column 'OrderID'
        dataType: int64
        isKey
        lineageTag: <guid>
        summarizeBy: none
        sourceColumn: OrderID

    column 'Amount'
        dataType: double
        lineageTag: <guid>
        summarizeBy: sum
        sourceColumn: Amount
        formatString: #,##0.00

    partition 'Sales-Partition' = m
        mode: import
        source = ```
                let
                    Source = Sql.Database("srv", "db"),
                    Sales  = Source{[Schema="dbo", Item="Sales"]}[Data]
                in
                    Sales
                ```
```

## Then add to `model.tmdl`

```tmdl
ref table 'Sales'
```

## Required pieces

- At least one `column` (PBI Desktop won't infer them from M via direct TMDL edit).
- Each `column` needs `sourceColumn:` matching the M output exactly (case-sensitive).
- A `partition` with `= m` and a `source` containing the M expression.
- `mode:` — typically `import`. See `../object-types/partition-properties.md` for `directQuery`, `dual`, `directLake`.

## Triple-backtick syntax

Use `` ``` `` fences for the M expression — preserves indentation and avoids needing to count tabs.

## After

`bash ../../../04-review/hooks/validate-tmdl.sh "<project>.SemanticModel"`. Reopen Desktop and refresh the table to load data.
