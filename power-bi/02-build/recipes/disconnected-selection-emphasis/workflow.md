# Workflow — assemble the recipe

Ordered build. Each step maps to a primitive and a [template](templates/). Substitute
[tokens](tokens.md) first. **Edit with Power BI Desktop closed**, then reopen to verify.

## Ordered file map

| # | Action | File | Primitive · Template |
|---|---|---|---|
| 1 | **Create** | `SemanticModel/definition/tables/<SELECTION_TABLE_NAME>.tmdl` | P1 · [selection-table.tmdl](templates/selection-table.tmdl) |
| 2 | **Append** before the `partition` line | `SemanticModel/definition/tables/<MEASURE_TABLE>.tmdl` | P2 · [boundary-measures.tmdl](templates/boundary-measures.tmdl) |
| 3 | **Append** after the last `ref table` | `SemanticModel/definition/model.tmdl` | P1 · [model-ref.tmdl](templates/model-ref.tmdl) |
| 4 | **Create** | `Report/definition/pages/<PAGE_ID>/visuals/<VISUAL_NAME_SLICER>/visual.json` | P5 · [slicer.visual.json](templates/slicer.visual.json) |
| 5 | **Create** | `Report/definition/pages/<PAGE_ID>/visuals/<VISUAL_NAME_CHART>/visual.json` | P3+P4+P5 · [chart-with-band.visual.json](templates/chart-with-band.visual.json) |

Steps 1–3 are the model layer (table + harvester measures + registration). Steps 4–5 are
the report layer (the slicer and the emphasised chart).

## Why this order

P1 must exist before P2 (measures reference the table) and before P3/P4 (the chart
aggregates the disconnected column / harvester measures). Register in `model.tmdl` (step 3)
or Desktop won't load the table. Visuals come last because they reference everything above.

## Validation

- Model view: `<SELECTION_TABLE_NAME>` has **no relationships** (the defining check).
- Slicer renders the expected picker (date "Between" / numeric range / category list).
- Chart shows **two Y series**: the clean main line + the gated series carrying labels/markers.
- Moving the slicer shifts the **shaded band and the visible labels together**.
- Tooltip exposes the harvester measures (the active selection is readable).
- `pbir validate "<project>.Report"` is clean (after step 5).

## Adapt for a variant

Pick a [variant](variants/) and apply its deltas to steps 1–5:
- [time-window-highlight](variants/time-window-highlight.md) — as-is (dates).
- [numeric-threshold-band](variants/numeric-threshold-band.md) — numeric source + slicer mode.
- [comparison-period-shading](variants/comparison-period-shading.md) — `SELECTEDVALUE` harvest, one line.
- [category-spotlight](variants/category-spotlight.md) — drop P3 shading; gate **color** in P4.

## Gotchas

- Triple-backtick `source` block in the table TMDL is indentation-sensitive in Desktop — keep exact, or use the one-line `VALUES(...)` form.
- Every `lineageTag` (UUID), `PBI_Id` (32-hex), visual `name` and `filter.name` (20-hex) must be **fresh and unique** — see [tokens.md](tokens.md).
- Desktop overwrites on-disk TMDL when it saves — close it before editing the model.
