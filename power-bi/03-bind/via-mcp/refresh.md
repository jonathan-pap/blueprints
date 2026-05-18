# Refresh the model (via MCP)

Trigger a data refresh — re-runs Power Query / M, reloads VertiPaq.

## Tool call

```
mcp__powerbi__refresh({
  workspace: "<workspace>",
  dataset:   "<model-name>",
  type:      "full",          // full | calculate | automatic | dataOnly
  tables:    ["Sales"]        // optional; omit for whole-model refresh
})
```

## Refresh types

| Type | Behaviour |
| --- | --- |
| `full` | Drop data, re-query source, recalculate DAX |
| `calculate` | Recalculate DAX only (no source query) |
| `automatic` | Engine decides per partition |
| `dataOnly` | Re-query source, skip DAX recalc |

## Async / sync

Most MCP refresh tools return a `refreshId` immediately and complete async. Poll the operations endpoint (or the MCP server's status tool) if you need to block on completion.

## Fallback (no MCP)

`../via-powershell/refresh-model.md` — TMSL `refresh` script via `$server.Execute()`, plus `scripts/refresh_model.py` wrapping the Enhanced Refresh REST API (Fabric models).

## When refresh fails

`../via-powershell/refresh-troubleshooting.md` — credentials, gateway, type/schema mismatches, timeouts, incremental refresh, capacity throttling, calculated-table errors, per-table isolation debugging.
