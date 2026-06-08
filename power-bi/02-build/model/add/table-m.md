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

## Pitfall — single-line `let…in` partition source triggers spurious "cyclic reference"

For a multi-step M expression, the source MUST be the canonical multi-line block. Writing it on one line:

```tmdl
    partition 'Sales' = m
        mode: import
        source = let Source = Csv.Document(...), Promoted = ..., Typed = ... in Typed   ← BROKEN
```

makes Power BI Desktop fail the load with *"A cyclic reference was encountered during evaluation"* — even though the M is a clean DAG (Source → Promoted → Typed) with no self-reference. The error blocks every table in the failing query's load-evaluation cluster, so it looks systemic, not per-table. `pbir model -d` / `tmdl-validate` accept the single-line form silently; only Desktop catches it.

The fix is the canonical multi-line shape Desktop itself writes — `source =` alone, then `let` / step lines / `in` / result each on their own line, indented **deeper than `source =`**, with **no triple-backticks**:

```tmdl
    partition 'Sales' = m
        mode: import
        source =
                let
                    Source = Csv.Document(File.Contents("E:/data/sales.csv"), [Delimiter=","]),
                    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
                    Typed = Table.TransformColumnTypes(Promoted, {{"Date", type date}, {"Amount", Currency.Type}})
                in
                    Typed
```

Single-line is only safe for a **single-expression** source (one `ROW(...)`, one `DATATABLE(...)`, one function call). Multi-step `let…in` always needs the multi-line block.

Reference shape: this file's example, and `projects/test/.../financials.tmdl`. Confirmed 2026-05-28 against a 13-table CSV splice that failed with cyclic-reference on single-line partitions and loaded all 14 tables cleanly after switching to multi-line.

## After

`bash ../../../04-review/hooks/validate-tmdl.sh "<project>.SemanticModel"`. Reopen Desktop and refresh the table to load data.
