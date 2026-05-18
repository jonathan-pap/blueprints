# Room 03 — Bind (live model)

> Live operations against a Power BI model. **Use this room only when on-disk TMDL is insufficient.** Most read needs are satisfied by `pbir model -d` from `../02-build/report/bind/find-canonical-name.md` (no connection required).

## Three-tier preference

1. **First** — `pbir model -d` on the on-disk TMDL. Works for thick PBIP projects. No connection. → `../02-build/report/bind/find-canonical-name.md`
2. **Second** — **Power BI MCP** for everything live: querying values, validating DAX live, modifying the model, refreshing. → `via-mcp/_index.md`
3. **Third** — **`connect-pbid`** (PowerShell / TOM / ADOMD) as alternative when MCP is unavailable, plus leverage points where MCP doesn't cover: field parameters, daxlib package mgmt, query traces, VertiPaq stats, Parallels-on-Mac. → `via-powershell/_index.md`

## When to enter (and which branch)

- **"What measures/columns exist?"** for thick PBIP → don't enter this room, use `../02-build/report/bind/find-canonical-name.md` (`pbir model -d`).
- **"What measures/columns exist?"** for thin PBIP / live → `via-mcp/list-measures.md`.
- **"Run this DAX query and show me the result"** → `via-mcp/query-dax.md`. Fallback: `via-powershell/query-dax.md`.
- **"Validate this DAX against the live engine"** → `via-mcp/query-dax.md`.
- **"Add this measure to the live model now"** → `via-mcp/add-measure.md`. Fallback: `via-powershell/modify-tom.md`.
- **"Trigger a refresh"** → `via-mcp/refresh.md`. Fallback: `via-powershell/refresh-model.md`.
- **"Create a field parameter"** → `via-powershell/field-parameter.md` (TOM-specific; rarely exposed by MCP).
- **"Install / use a daxlib package"** → `via-powershell/daxlib.md` (PowerShell-only).
- **"Trace what DAX a visual is generating"** → `via-powershell/query-listener.md` (TOM trace API).
- **"VertiPaq column/table sizes"** → `via-powershell/vertipaq-stats.md` (DMV via ADOMD).
- **"Mac via Parallels"** → `via-powershell/parallels-macos.md`.
- **"Install / configure live-model validation hooks"** (DAX refs, measure metadata, RI, compat level) → `via-powershell/hooks/_index.md`.

## Hard rules

- Mutations are not undoable in Power BI Desktop. Test on a backup first.
- Never modify model metadata without explicit user direction.
- Always close the connection / session after use.
- `pbir` CLI handles thick-project reads without a live connection — use it whenever possible.

## What's here

- `via-mcp/` — Power BI MCP tool calls (preferred for live ops)
- `via-powershell/` — connect-pbid PowerShell scripts + atomic guides (alternative + leverage points)
- `_index.md` — full atomic picker
