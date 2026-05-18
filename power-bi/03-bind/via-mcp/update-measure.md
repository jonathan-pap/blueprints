# Update a measure (via MCP)

Change an existing measure's DAX or properties.

## Tool call

```
mcp__powerbi__update_measure({
  workspace:    "<workspace>",
  dataset:      "<model-name>",
  table:        "<table-name>",
  name:         "Total Revenue",
  expression:   "SUMX('Sales', 'Sales'[Qty] * 'Sales'[Price])",
  formatString: "#,##0.00"
})
```

Omit fields you don't want to change.

## Before calling

- `list-measures.md` to confirm the current state (so you know what you're overwriting).
- `validate-dax.md` to syntax-check the new expression.

## After calling

- Mirror the change to disk via `../../02-build/model/` — otherwise the next reload of the project file overwrites it.
- Any visual bound to this measure will re-evaluate. If the format string changed, may need to refresh visuals to see the new format.

## Fallback (no MCP)

`../via-powershell/modify-tom.md` — set `$measure.Expression = "..."` and `SaveChanges()`.
