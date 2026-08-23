# Room 02 — Build

> Edit the PBIP project files. No live model connection from this room (that's `../03-bind/`). Power BI Desktop will pick up changes when the user closes and reopens the file.

## When to enter

User has a locked brief (from `../01-brief/`) and wants to actually modify report/model/theme/visual files.

## Sub-room router

Match the task to one sub-room. Enter one sub-room at a time. Each sub-room has its own `context.md` and `references/`.

| Task | Sub-room |
|---|---|
| Add / move / format / bind visuals; create pages; edit layout | `report/` |
| Add or change measures, columns, tables, relationships, hierarchies | `model/` |
| Change colors, fonts, default styles for all visuals of a type | `theme/` |
| Build a custom visual that native Power BI can't express | `visuals/` then pick engine |
| Apply a multi-step composed pattern that spans model + report | `recipes/` then pick a recipe |

### Recipes (cross-room compositions)

Self-contained, atomized patterns that combine model + report primitives. Each recipe has its own `context.md`, atomic `primitives/`, `variants/`, `templates/`, and a worked `examples/`.

- `recipes/disconnected-selection-emphasis/` — a disconnected slicer harvested into boundary measures that drive visual emphasis (reference-band shading + a gated series) **without filtering**. Variants: time-window highlight, numeric threshold band, comparison-period shading, category spotlight.
- `recipes/pareto-chart/` — a sorted column + cumulative-% line that splits at the 80% mark ("vital few vs. trivial many"), built entirely from **visual calculations** (no model changes). The trick is `RUNNINGSUM(..., ORDERBY([value], DESC))`. Variants: dynamic threshold, ABC classification, count Pareto, model-measure Pareto.
- `recipes/actual-vs-target-variance/` — a native clustered column that reads as an actual-vs-target variance chart: outlined target + filled actual bars with **directional green/red connectors drawn from repurposed error bars**, a ▲/▼ % label, and a narrative subtitle. Native visuals only. Variants: vs prior year, tolerance band (RAG), horizontal by category, minimal.
- `recipes/candlestick/` — an OHLC **candlestick** (Power BI has **no native** one) built from a native `lineStackedColumnComboChart`: bodies = a transparent **floater** + a stacked body column (green up / red down), wicks = **error bars** off invisible High/Low lines (`High/Low Distance`), with both value axes **locked to `MinY/MaxY`** so bodies and wicks share scale. Fully interactive. Needs a real OHLC fact (Open/High/Low/Close per period) — shipped example: grand-exchange `FactMarketPriceDaily`. Variants: volume pane, hollow up-candles (IBCS), Heikin-Ashi, OHLC bars, inline-SVG (static, table-cell).
- `recipes/waterfall/` — a DAX-driven waterfall on a native `lineStackedColumnComboChart` (or `barChart` for horizontal). A **disconnected steps table** + per-step `IF SELECTEDVALUE` body measures drive totals/drops via a transparent floater. Variants: vertical/horizontal × standard/detailed labels, plus stacked composition for steps that split into tier-coherent sub-segments. **Interactive recipe** — asks the user for steps + types + sources + orientation + label style BEFORE generating any DAX.

## Decision rules

- **Theme vs visual override:** If the change should apply to every visual of a type, edit `theme/`. If it's a single-visual exception, edit `report/`.
- **Model vs report extension:** If the measure is reusable, add it to the model via `model/`. If it's report-specific only, add a thin-report measure via `report/calculations/thin-report-measure.md`.
- **Native vs custom visual:** Try native visuals first. Only enter `visuals/` when native cannot express the chart.
- **Need real field/measure names?** Stop. Load `../03-bind/context.md`, get the names, come back.

## Hard rules across all sub-rooms

- All PBIP files are **UTF-8 without BOM**. A BOM breaks parsers.
- After every mutation in `report/`, run `pbir validate "<project>.Report"`.
- After every mutation in `model/`, validate TMDL syntax (see `model/context.md`).
- Never edit `.pbi`/`.platform` files unless explicitly intended — they carry IDs.
- Renames cascade: a table or measure rename touches TMDL, visual JSON, report extensions, culture files, and DAX query files. See `report/pbip-format/_index.md` (rename cascades) and `model/naming/_index.md`.
- Tell the user to close and reopen Power BI Desktop after the change — it does not detect external file edits.
- **Desktop must be CLOSED before editing TMDL on disk.** Desktop holds an in-memory copy of the model; its next save (or close-with-save) writes that copy back to disk and silently overwrites every external edit. Confirm Desktop is closed before each `model/` mutation, or tell the user to close it first. After editing, if Desktop was open during the edits, close it WITHOUT saving so the stale copy doesn't clobber the new files. A clean `pbir model -d` immediately after editing proves the on-disk state is good but does NOT protect it from a later Desktop save. Symptom of a clobber: `<system-reminder>` notes that a file you just wrote was "modified by user or linter" — that's the overwrite signature. Confirmed against gddt 2026-05-21 (lost calc columns + `dim_calendar` + `_Measures` + relationships to one Desktop save).

## Project layout you're editing

```
projects/<name>/
├── <name>.Report/         ← report/ sub-room writes here
├── <name>.SemanticModel/  ← model/ sub-room writes here
└── <name>.pbip
```

The theme JSON lives inside `<name>.Report/StaticResources/`. Custom visuals (Deneb/SVG/Python/R) are wired through `<name>.Report/` visual.json files but their source artifacts live alongside the project.

## Outputs

This room produces edits in `projects/<name>/`. Any generated artifacts (audit logs, DAX traces, exports) belong in `../outputs/` with `YYYY-MM-DD-<project>-<type>.<ext>` naming.
