# Tabular Editor Blueprint

A self-contained toolkit of **C# scripts, Best-Practice-Analyzer rule sets, and macros** for Tabular
Editor — every one written to run **unchanged in Tabular Editor 2 (free) and Tabular Editor 3**.

Works on **any tabular model**: Power BI (PBIP/TMDL or live), Azure Analysis Services, SSAS, Fabric.

## Quick start

1. Install Tabular Editor 2 (free, [github.com/TabularEditor/TabularEditor](https://github.com/TabularEditor/TabularEditor)) and/or Tabular Editor 3.
2. Open your model — TE3 opens a **PBIP/TMDL** folder directly; TE2 uses a `.bim` or a **live**
   `localhost:<port>` connection.
3. Run a script from `scripts/`, a rule set from `bpa/`, or a macro from `macros/` — see [`run.md`](run.md).
4. **Save** (Ctrl+S) to persist model changes.

Point Claude (or your agent) at this folder and tell it to read [CLAUDE.md](CLAUDE.md).

## What's here

| Folder | Contents |
|---|---|
| [`scripts/`](scripts/) | C# advanced scripts — bulk formatting, time-intelligence, documentation, cleanup |
| [`bpa/`](bpa/) | Best Practice Analyzer rule sets (`.json`) + authoring/running guide |
| [`macros/`](macros/) | TE3 macros (UI-bound actions) |
| [`compatibility.md`](compatibility.md) | the TE2 ⇄ TE3 "works in both" ruleset — read before writing |
| [`run.md`](run.md) | run from the UI, CLI (`TabularEditor.exe` / `TabularEditor3.exe`), or CI |

## Why one blueprint per tool

Tabular Editor operates across many model hosts, so it lives at the workspace root as its own blueprint —
zip it, drop it beside any tabular model, it works. The `power-bi/` blueprint cross-references it for the
Power BI workflow; nothing here depends on Power BI.

## The portability contract

TE2 ships an older C# compiler and a smaller API than TE3. Everything here sticks to **C# 7 syntax, the
shared API surface, `Output()` for feedback, and a whole-model fallback for `Selected.*`** so it runs in
both — and headless (CLI/CI). Details + a pre-commit checklist: [`compatibility.md`](compatibility.md).
