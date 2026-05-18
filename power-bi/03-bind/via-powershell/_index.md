# via-powershell/ — atomic files

> Alternative path when Power BI MCP isn't available, plus leverage points where TOM/ADOMD does things MCP rarely exposes.

## Entry points

- `quickstart.md` — port discovery, NuGet install, first connection
- `query-dax.md` — ADOMD.NET query patterns
- `modify-tom.md` — buffered TOM mutations + SaveChanges

## Leverage points (PowerShell-specific value)

- `field-parameter.md` — TOM-specific calculated-table pattern (no clean MCP equivalent)
- `daxlib.md` — DAX library / UDF package mgmt
- `query-listener.md` — TOM trace API for capturing visual queries
- `evaluateandlog-debugging.md` — `EVALUATEANDLOG` step trace
- `performance-profiling.md` — server timings, query plan
- `vertipaq-stats.md` — DMV-based storage stats
- `load-tmdl-files.md` — apply a TMDL fragment via TOM
- `export-model.md` — full model snapshot to disk

## DAX semantics

- `dax-expressions.md` — common DAX shapes
- `dax-pitfalls.md` — common DAX bugs when querying programmatically
- `calendar-column-groups.md` — date table conventions

## Operational

- `annotations.md` — read/write per-object annotations
- `refresh-model.md` — refresh via TMSL / RequestRefresh
- `parallels-macos.md` — running Desktop on Mac via Parallels

## Per-object TOM CRUD

- `tom-object-types/_index.md` → split per object type (measure, column, table, relationship, role, perspective, etc.)

## Scripts

`scripts/` contains executable `.ps1` and `.sh` files. Use these as canned end-to-end flows; read individually only when modifying.

## Live-model validation hooks

`hooks/_index.md` — PreToolUse / PostToolUse hooks that fire on Bash commands touching the live model: DAX reference validation, measure metadata enforcement, referential integrity after `SaveChanges`, compatibility-level nudge, model-metadata cache refresh. Different from `../../04-review/hooks/` (which validates files on disk).
