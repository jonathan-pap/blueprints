# Read a measure's DAX definition

Pull the full TMDL block (DAX + format string + display folder + annotations) from disk.

## Single measure

```bash
awk '/^\s*measure '\''Total Revenue'\''/,/^[^[:space:]]/' \
  "<project>.SemanticModel/definition/tables/Sales.tmdl"
```

## All measures in a table

```bash
awk '/^\s*measure / {flag=1} flag {print} /^$/ {flag=0}' \
  "<project>.SemanticModel/definition/tables/Sales.tmdl"
```

## Read with context (display folder, format)

A measure block looks like:

```tmdl
measure 'Total Revenue' =
        SUM('Sales'[Amount])
    formatString: #,##0
    displayFolder: 1. Revenue
    lineageTag: abc-123
```

- DAX body: indented 2 levels deeper than the declaration (see `../../model/context.md` critical rules).
- Properties: at depth 2.
- `lineageTag`: never modify existing values.

## When to escalate

- DAX has a bug → `../../../03-bind/references/evaluateandlog-debugging.md`
- Need to compute the live result → `../../../03-bind/references/query-dax.md`
