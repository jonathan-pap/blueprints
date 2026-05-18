# List measures (via MCP)

Get canonical measure names + DAX. Required input for any bind to a measure role.

## Tool call

```
mcp__powerbi__list_measures({
  workspace: "<workspace>",
  dataset:   "<model-name>",
  table:     "<table-name>"     # optional; omit for all tables
})
```

Returns: `name`, `tableName`, `expression` (DAX), `formatString`, `displayFolder`, `isHidden`, `description`.

## Common follow-ups

- Take the returned `name` + `tableName` and feed into `../../02-build/report/bind/bind-field.md` with `-t Measure`.
- If the DAX returned isn't what you expected, `update-measure.md` to fix it live, or `../../02-build/model/` to fix the TMDL on disk.

## Filter to one table

Saves tokens for large models. Always pass `table` when you know it.

## Fallback (no MCP)

- Thick PBIP → `../../02-build/report/bind/find-canonical-name.md` already shows all measures.
- Otherwise → `../via-powershell/query-dax.md` with DMV: `SELECT * FROM $SYSTEM.TMSCHEMA_MEASURES`.
