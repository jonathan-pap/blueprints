# Room — Tabular Editor (C# scripts, TE2 + TE3)

> Reusable **C# scripts** that operate on the semantic model via Tabular Editor's scripting API.
> Every script here is written to run **unchanged in both Tabular Editor 2 (free) and Tabular
> Editor 3**. Use this room for **bulk model operations** that would be tedious one-at-a-time:
> mass-formatting measures, generating time-intelligence, hiding technical columns, documenting the
> model, applying Best-Practice fixes.

## When to enter this room

- You want to change **many** model objects at once (format every measure, add PY/YTD for a set of
  measures, hide all key columns) → a script beats hand-editing TMDL or one-by-one MCP calls.
- You want a **repeatable** model operation you can re-run on any project or in CI.
- You want Tabular Editor's **Best Practice Analyzer** fixes as code.

For single, surgical changes prefer the other rooms:

| Need | Go to |
|---|---|
| One measure / column / relationship, live | `../03-bind/` (Power BI Modeling MCP) |
| Hand-edit a few TMDL objects, Desktop closed | `../02-build/model/` |
| **Bulk / repeatable model ops via script** | **here** |

## How it fits

Tabular Editor scripts run against **the semantic model** — either an open **PBIP/TMDL** folder
(TE3 natively; TE2 via a saved `.bim` or a live connection) or a **live connection** to the model
hosted by Power BI Desktop (same local instance the `03-bind/` MCP/TOM path uses). Changes are applied
to the in-memory model and persisted when you **save** (UI) or pass a save flag (CLI). Validate the
result with `../04-review/` afterwards.

## The one rule that makes a script portable

**Write to the shared TE scripting surface + C# 7-safe syntax only.** TE2 and TE3 both run Roslyn,
but TE2 ships an older compiler and a smaller API. A script that avoids TE3-only APIs and modern C#
syntax runs in both. The full ruleset — and the exact do/don't list — is in
[`compatibility.md`](compatibility.md). How to run them (UI, CLI, CI): [`run.md`](run.md).

## Files

- [`compatibility.md`](compatibility.md) — the TE2 ⇄ TE3 "works in both" ruleset (read first)
- [`run.md`](run.md) — run a script from the UI, the CLI (`TabularEditor.exe` / `TabularEditor3.exe`), or CI
- [`scripts/`](scripts/) — the script library ([`scripts/_index.md`](scripts/_index.md))

## After

Run `../04-review/` (validate / model-audit / BPA) — a bulk script touches many objects; verify.
