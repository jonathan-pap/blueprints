# Is a Power BI MCP server available?

Power BI MCP servers expose model operations as MCP tools (e.g. `mcp__powerbi__list_tables`). Check before assuming they're wired.

## Detect from the agent side

Look in the available tool list for tool names starting with `mcp__powerbi__`, `mcp__pbi__`, `mcp__fabric__`, or similar.

If using the SDK's `ToolSearch`, query:

```
ToolSearch("powerbi" or "pbi" or "fabric") → returns 0 = no MCP
```

## If not available

Two paths:

1. **For thick PBIP read operations**: skip this room entirely. Use `pbir model -d` from `../../02-build/report/bind/find-canonical-name.md`.
2. **For everything else**: fall back to `../via-powershell/quickstart.md`.

## If available

Continue to `list-tables.md` (or whichever read/write step you need). The actual tool name will be slightly different per MCP server — e.g.:

| Generic name in our docs | Possible real tool name |
| --- | --- |
| `list_tables`            | `mcp__powerbi__list_tables`, `mcp__pbi__model_tables`, `mcp__fabric__list_dataset_tables` |
| `query_dax`              | `mcp__powerbi__query_dax`, `mcp__pbi__execute_dax` |
| `add_measure`            | `mcp__powerbi__add_measure`, `mcp__pbi__create_measure` |

Match by intent, not by exact name.
