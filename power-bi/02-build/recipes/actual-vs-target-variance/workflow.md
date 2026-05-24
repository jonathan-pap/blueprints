# Workflow — assemble the recipe

Model layer first (the measures), then one combo visual. Substitute [tokens](tokens.md)
first. **Edit with Power BI Desktop closed**, then reopen to verify.

## Ordered file map

| # | Action | File | Primitive · Template |
|---|---|---|---|
| 1 | **Append** before the `partition` line | `SemanticModel/definition/tables/<MEASURE_TABLE>.tmdl` | P1 · [variance-measures.tmdl](templates/variance-measures.tmdl) |
| 2 | *(optional)* **Append** the narrative measures | same file | P5 · [variance-measures.tmdl](templates/variance-measures.tmdl) |
| 3 | *(optional)* **Create / append** the format UDF | `SemanticModel/definition/functions.tmdl` | — · [dynamic-format-udf.tmdl](templates/dynamic-format-udf.tmdl) |
| 4 | **Create** the chart | `Report/definition/pages/<PAGE_ID>/visuals/<VISUAL_NAME_CHART>/visual.json` | P2·P3·P4 · [actual-vs-target.visual.json](templates/actual-vs-target.visual.json) |

Step 1 is the only required model edit. Steps 2–3 add the narrative subtitle and dynamic K/M/B
number formatting — skip them for the [minimal variant](variants/minimal-no-narrative.md).

## Why this order

- **Measures before the visual.** The chart binds `<ACTUAL>`, `<TARGET>`, `MAX VALUE`,
  `GREEN MAX`, `RED MAX` (Y series + error-bar bounds) and `% Delta` / `Delta Color` (labels).
  All must exist first or the bindings break.
- **`MAX VALUE` before `GREEN MAX`/`RED MAX`** — the latter two reference it.
- **UDF before the measures that use it** (`formatStringDefinition = DYNAMIC_FORMATING_INDICATORS()`)
  — and the model must be **compatibilityLevel 1601+** for any `formatStringDefinition` (see
  the gotcha below).

## Validation

- Three series render: outlined **target**, filled **actual**, and an invisible **MAX** (you
  see only its label).
- Each period shows a **green connector** (actual above target) **or** a **red connector**
  (actual below) — never both.
- The ▲/▼ **% label** sits at the top of the taller bar, green when up / red when down.
- The subtitle reads as a sentence ("…beat target in N months…").
- `pbir validate "<project>.Report"` is clean.

## Adapt for a variant

- [yoy-variance](variants/yoy-variance.md) — replace `<TARGET_MEASURE>` with a prior-year measure.
- [tolerance-band-rag](variants/tolerance-band-rag.md) — widen `Delta Color` / the connectors to a neutral zone.
- [horizontal-by-category](variants/horizontal-by-category.md) — `clusteredColumnChart` → `barChart`, category column instead of date.
- [minimal-no-narrative](variants/minimal-no-narrative.md) — skip steps 2–3 and the subtitle binding.

## Gotchas

- **Error bars are the connector** — they live in `objects.error`, bound per series with
  `errorRange.explicit.upperBound = <GREEN MAX / RED MAX>` and `isRelative: false`. Miss the
  `dataViewWildcard` selector and they won't render per category. See [P3](primitives/error-bar-variance-connector.md).
- **`MAX VALUE` series must be transparent** (`fillTransparency: 100`), not removed — it's what
  positions the % label above whichever bar is taller and reserves headroom. See [P2](primitives/overlay-series-scaffold.md).
- **`formatStringDefinition` needs compatibilityLevel ≥ 1601** in `database.tmdl`, and the
  arrow format `"▲0%;▼0%;0%"` must be a block-form definition, not an inline `formatString`
  (Desktop throws *"Invalid indentation"* otherwise). See `../../../model/update/multi-line-dax.md`.
- Every `lineageTag` / visual `name` must be fresh and unique — see [tokens.md](tokens.md).
