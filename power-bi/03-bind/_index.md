# 03-bind — atomic file index

> Three-tier preference: on-disk TMDL → Power BI MCP → connect-pbid PowerShell.

## via-mcp/  (preferred for all live operations)

- `check-mcp-available.md` — detect whether a Power BI MCP server is wired up
- `list-tables.md` — enumerate model tables
- `list-measures.md` — enumerate measures (canonical names + DAX)
- `list-columns.md` — enumerate columns of a table
- `query-dax.md` — run a DAX query against the live model
- `validate-dax.md` — syntax-check a DAX expression without running it
- `add-measure.md` — create a measure in the live model
- `update-measure.md` — change an existing measure's DAX or properties
- `delete-measure.md` — remove a measure
- `refresh.md` — trigger a model refresh

## via-powershell/  (alternative + leverage points)

- `quickstart.md` — port discovery, NuGet install, first connection
- `query-dax.md` — ADOMD.NET query patterns
- `modify-tom.md` — buffered TOM mutations + SaveChanges
- `tom-object-types.md` — per-object-type CRUD reference
- `field-parameter.md` — TOM-specific calculated-table pattern
- `daxlib.md` — DAX library package mgmt (PowerShell-only)
- `query-listener.md` — TOM trace API for capturing visual queries
- `evaluateandlog-debugging.md` — step-by-step DAX debug
- `performance-profiling.md` — server timings, query plan
- `vertipaq-stats.md` — DMV-based storage stats
- `annotations.md` — read/write per-object annotations
- `calendar-column-groups.md` — date-table conventions
- `dax-expressions.md` — DAX semantics quick ref
- `dax-pitfalls.md` — common DAX bugs when querying programmatically
- `export-model.md` — full model snapshot to disk
- `load-tmdl-files.md` — apply a TMDL fragment via TOM
- `refresh-model.md` — refresh via TMSL / RequestRefresh
- `parallels-macos.md` — running Desktop in Parallels on Mac

## scripts/ (PowerShell)

Inside `via-powershell/scripts/`:

- `connect-and-enumerate.ps1`, `explore-model.ps1`, `query-dax.ps1`, `debug-dax.ps1`, `refresh-table.ps1`, `modify-tom-objects.ps1`, `load-tmdl.ps1`, `create-field-parameter.ps1`, `connect-from-mac.sh`, `daxlib.sh`, `daxlib-tom/`

## hooks/ (live-model validation)

Inside `via-powershell/hooks/`:

- `_index.md` — picker for the hooks subsystem
- `overview.md` — the 5 hooks (validate-dax, validate-measure, refresh-cache, check-ri, check-compat) and when each fires
- `config.md` — toggle individual checks via `config.yaml`
- `degradation.md` — skip conditions (no jq, no PowerShell, missing cache, etc.)
- `windows-issues.md` — known Claude Code Bash-hook bugs on Windows + master kill-switch
- `testing.md` — fire a hook by hand
- `pbi-hooks.sh`, `snapshot-model.ps1`, `check-referential-integrity.ps1`, `hooks.json`, `config.yaml` — the scripts and Claude Code hook registration
