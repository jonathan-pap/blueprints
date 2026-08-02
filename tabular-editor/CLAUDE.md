# Tabular Editor Blueprint — Master Map

> Read this file first. A self-contained toolkit of **C# scripts, BPA rule sets, and macros** for
> Tabular Editor, all written to run **unchanged in Tabular Editor 2 (free) and Tabular Editor 3**.
> Operates on **any tabular model** — Power BI (PBIP/TMDL or live), Azure AS, SSAS, Fabric.

## What this blueprint is

- **Target tool:** Tabular Editor 2 (free) + Tabular Editor 3 (paid).
- **Operates on:** the semantic/tabular model — an open **PBIP/TMDL** folder (TE3), a `.bim` file, or a
  **live connection** (`localhost:<port>`, Azure AS, Fabric XMLA).
- **Portability contract:** every script/rule here runs in **both TE2 and TE3**. The rule that makes
  that true is in [`compatibility.md`](compatibility.md) — read it before writing anything.
- **Standalone:** zip this folder, drop it next to any tabular model, it works. The `power-bi/`
  blueprint cross-references it for the Power BI workflow, but nothing here depends on it.

## Capabilities

- `scripts/` — **C# advanced scripts** for bulk model ops (mass-format, time-intelligence, hide keys,
  documentation). Index: [`scripts/_index.md`](scripts/_index.md).
- `bpa/` — **Best Practice Analyzer** rule sets (`.json`) + how to author and run them. Index:
  [`bpa/_index.md`](bpa/_index.md).
- `macros/` — **TE3 macros** (saved actions/scripts bound to the UI). Index:
  [`macros/_index.md`](macros/_index.md). *(TE3-oriented; keep the logic TE2-portable where you can.)*

## Routing table

Match intent; load only what's listed.

- **Write / run a bulk model script (format many measures, add time-intelligence, hide keys, document)** → [`context.md`](context.md) → [`scripts/_index.md`](scripts/_index.md)
- **Author or run a BPA rule set** → [`bpa/_index.md`](bpa/_index.md)
- **Build a TE3 macro** → [`macros/_index.md`](macros/_index.md)
- **"Will this run in TE2 as well as TE3?"** → [`compatibility.md`](compatibility.md)
- **How do I run a script / rule (UI, CLI, CI)?** → [`run.md`](run.md)

## Hard rules (apply everywhere)

- **Portability first.** C# 7 syntax only, shared TE API surface only, feedback via `Output()`, and a
  whole-model fallback for `Selected.*` so scripts run headless. Full list: [`compatibility.md`](compatibility.md).
- **Never call `SaveChanges()` in a script.** Scripts mutate the in-memory model; TE persists on **save**
  (UI Ctrl+S) or a CLI save flag.
- **Test in TE2 first.** TE2 is the stricter compiler + smaller API — if it runs there, TE3 is fine.
- **Model-source-agnostic.** Scripts touch objects, not files; the same `.cs` runs whether the model was
  opened as PBIP/TMDL, `.bim`, or a live connection.

## Working on a Power BI model

Point Tabular Editor at a `power-bi/` project's `projects/<name>.SemanticModel` (TE3 opens the TMDL
folder; TE2 connects live to the open Desktop instance — find the port via
[`../power-bi/03-bind/via-powershell/quickstart.md`](../power-bi/03-bind/via-powershell/quickstart.md)
or the Modeling MCP `connection_operations`). After a bulk change, reload/verify with
[`../power-bi/03-bind/desktop-bridge.md`](../power-bi/03-bind/desktop-bridge.md) and
[`../power-bi/04-review/`](../power-bi/04-review/).
