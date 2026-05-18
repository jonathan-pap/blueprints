# List columns (via MCP)

Get canonical column names + types for one table.

## Tool call

```
mcp__powerbi__list_columns({
  workspace: "<workspace>",
  dataset:   "<model-name>",
  table:     "<table-name>"
})
```

Returns: `name`, `dataType`, `summarizeBy`, `isHidden`, `displayFolder`, `sortByColumn`, `isKey`.

## Use the output to

- Bind a column to a visual role → `../../02-build/report/bind/bind-field.md` with `-t Column`.
- Decide if `summarizeBy` needs to flip (`none` for keys/attributes, `sum` for additive facts) → `../../02-build/model/_index.md`.

## Fallback (no MCP)

- Thick PBIP → `../../02-build/report/bind/find-canonical-name.md`.
- Otherwise → DMV: `SELECT * FROM $SYSTEM.TMSCHEMA_COLUMNS WHERE [TableID] = <id>` via `../via-powershell/query-dax.md`.
