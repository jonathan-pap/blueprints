# List tables (via MCP)

Enumerate model tables to discover canonical names before binding.

## Tool call

Use the Power BI MCP tool whose intent matches `list_tables`. Typical signature:

```
mcp__powerbi__list_tables({
  workspace: "<workspace>",
  dataset:   "<model-name>"
})
```

Returns an array of table objects, each with at least `name` (canonical) and optionally `description`, `isHidden`, `columnCount`, `measureCount`.

## When working with a thin PBIP

Read the connection target from the project's `definition.pbir`:

```bash
jq -r '.datasetReference.byConnection' "<project>.Report/definition/definition.pbir"
```

The returned object names the workspace + model — feed those into the MCP call.

## Fallback (no MCP)

- Thick PBIP → `../../02-build/report/bind/find-canonical-name.md` (`pbir model -d`).
- Otherwise → `../via-powershell/quickstart.md` then `../via-powershell/tom-object-types.md`.
