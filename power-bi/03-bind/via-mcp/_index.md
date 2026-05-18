# via-mcp/ — atomic files

> Power BI MCP is the preferred path for all live model operations. Tool names below are generic — your installed MCP server may use slightly different names. Use `check-mcp-available.md` first to confirm what's wired up.

## Detect

- `check-mcp-available.md` — is a Power BI MCP server connected?

## Read

- `list-tables.md` — model tables
- `list-measures.md` — measures (canonical names + DAX)
- `list-columns.md` — columns of a table
- `query-dax.md` — run a DAX query
- `validate-dax.md` — syntax-check without running

## Write

- `add-measure.md` — create a measure
- `update-measure.md` — change DAX or properties
- `delete-measure.md` — remove a measure
- `refresh.md` — trigger a refresh

## Rule

Power BI MCP is the default for everything live. Drop to `../via-powershell/` only when:
- MCP is not installed / not connected (`check-mcp-available.md` returns no)
- The operation needs a feature MCP doesn't expose (field parameters, daxlib, query trace, VertiPaq stats)
