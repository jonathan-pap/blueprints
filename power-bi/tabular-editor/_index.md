# tabular-editor — atomic file index

> Reusable C# scripts for **bulk** semantic-model operations, portable across **Tabular Editor 2 & 3**.
> Enter from [`context.md`](context.md). For single edits use `../03-bind/` (MCP) or `../02-build/model/`.

## Room docs

- [`context.md`](context.md) — what this room is, when to use it, how it fits the pipeline
- [`compatibility.md`](compatibility.md) — the TE2 ⇄ TE3 "works in both" ruleset (C# 7 + shared API + `Output()` + headless fallback)
- [`run.md`](run.md) — run from the UI, the CLI (`TabularEditor.exe` / `TabularEditor3.exe`), or CI

## Scripts — [`scripts/`](scripts/) ([`scripts/_index.md`](scripts/_index.md))

- `format-measures.cs` — mass format + display-folder measures
- `create-time-intelligence.cs` — PY / YTD / YoY% per base measure
- `document-model.cs` — measures → Markdown
- `hide-technical-columns.cs` — hide keys, `SummarizeBy=None` on numeric keys

## Model source

TE3 opens the PBIP/TMDL folder directly; TE2 uses a `.bim` or a **live** `localhost:<port>` connection
(same instance as `../03-bind/`). Scripts touch objects, not files, so the same `.cs` runs either way.
