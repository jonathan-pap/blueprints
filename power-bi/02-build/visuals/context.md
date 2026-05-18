# Sub-room — Custom Visuals

> Used when native Power BI visuals cannot express the chart. Each engine has trade-offs — pick before building.

## Decision: which engine?

- **Advanced interactive chart (cross-filter, hover, tooltips)** → **Deneb** (Vega / Vega-Lite). Declarative, integrates with Power BI selection model.
- **Inline graphics in tables/matrices/cards (sparklines, data bars, status pills, progress bars)** → **SVG** (via DAX measure). No custom visual registration, lightweight.
- **Statistical chart (distribution, regression, correlation)** → **Python** (matplotlib / seaborn). Static PNG, strong statistical libraries.
- **R-ecosystem chart (forecast, pheatmap, corrplot)** → **R** (ggplot2). Static PNG, R-specific libraries.

If two engines could do the job, prefer in this order: **SVG → Deneb → Python → R**. SVG is lightest, Deneb is most capable, Python/R lose interactivity.

## Engines (sub-rooms)

- **`deneb/`** — interactive custom visual via Vega or Vega-Lite
- **`svg/`** — inline SVG via DAX extension measures, rendered as ImageUrl
- **`python/`** — matplotlib / seaborn script for static statistical visual
- **`r/`** — ggplot2 script for static statistical visual

## Rules across all engines

- Custom visuals reduce report interactivity (Python/R: no cross-filter; SVG: no interaction).
- Always check whether a native visual + theme override would solve the problem first (`../report/` + `../theme/`).
- For SVG measures specifically: the DAX measure must return a `data:image/svg+xml;utf8,...` string and the measure's `dataCategory` must be `ImageUrl`.
- All custom visuals still need field bindings — discover canonical field names via `../report/semantic-model/find-field-from-tmdl.md` (on-disk) or `../../03-bind/via-mcp/list-measures.md` (live) before writing.
