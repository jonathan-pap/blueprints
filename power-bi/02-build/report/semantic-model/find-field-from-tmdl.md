# Find a field's canonical name from TMDL

Read `<project>.SemanticModel/definition/tables/*.tmdl` to discover the exact table and field names without a live connection.

## Grep one table

```bash
grep -E "^\s*(measure|column) " "<project>.SemanticModel/definition/tables/Sales.tmdl"
```

## Find a measure across all tables

```bash
grep -rE "^\s*measure 'Total Revenue'" "<project>.SemanticModel/definition/tables/"
```

## List all measures in the model

```bash
grep -rE "^\s*measure " "<project>.SemanticModel/definition/tables/" | sort -u
```

## Output format

TMDL uses single-quoted names when they contain spaces or special chars:

```tmdl
table 'Sales'
    measure 'Total Revenue' = SUM('Sales'[Amount])
        formatString: #,##0
```

Bind with `-a "Y:Sales.Total Revenue" -t Measure` (CLI handles the quoting internally).

## Why this beats live connection

- Works without Power BI Desktop open
- Works on a Git branch
- No port discovery, no NuGet install
- Same canonical names

For live values, go to `../../../03-bind/references/quickstart.md`.
