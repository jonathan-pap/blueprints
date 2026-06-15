# add-visual/ — atomic files

> One file per chart type. Each ≤ 40 lines. Each links to a copy-ready template under `../examples/visuals/`.

## Single-value

- `kpi-card.md` — KPI with target + trend (preferred when a target exists)
- `card.md` — simple headline number, no target

## Comparison & trend

- `line-chart.md` — time series
- `bar-chart.md` — horizontal, long labels
- `column-chart.md` — vertical, short labels
- `clustered-column-chart.md` — multi-series categories
- `combo-chart.md` — line + column (two scales)
- `area-chart.md` — filled trend / stacked area
- `waterfall-chart.md` — variance bridge

## Part-to-whole

- `donut-chart.md` — single split, max 5 slices

## Correlation

- `scatter-chart.md` — two continuous axes

## Geographic

- `map.md` — `azureMap` (the default; legacy `map`/`filledMap`/`shapeMap` are deprecated)

## Records & detail

- `table.md` — flat row list (`tableEx`)
- `matrix.md` — hierarchical, multi-dimensional (`pivotTable`)

## Indicators / dials

- `gauge.md` — actual against min/max bounds

## Selection / navigation

- `slicer.md` — page-level filter as a visual
- `action-button.md` — bookmark / navigation / drillthrough trigger

## Non-data

- `textbox.md` — page titles, captions
- `image.md` — logos, illustrations
- `shape.md` — separators, dividers, callout backgrounds

## Decision help

- `pick-visual-type.md` — "what visual answers this reader question?"

## Templates library

`../examples/visuals/`:

- `default/` — 20 minimal visual.json templates (theme defaults only)
- `formatted/` — 35 templates with formatting, conditional formatting, filters, advanced patterns
- `__index.md` — full template catalogue with descriptions

## Common rules

- Run `../bind/find-canonical-name.md` BEFORE creating any data visual.
- Run `../validate/validate.md` AFTER each addition.
- **Bind inline with `-d "Role:Table.Field"`** on the same `pbir add visual` call (repeatable for multiple
  roles) — it's the one-shot path the per-visual files split into a separate `pbir visuals bind` step.
  Both work; inline is fewer calls. Roles are the type's exact role names (`pbir add visual --list`):
  e.g. `cardVisual`→`Data`, charts→`Category`/`Y`/`Y2`, `scatterChart`→`X`/`Y`, `gauge`→`Y`/`TargetValue`,
  `tableEx`/`slicer`→`Values`, `pivotTable`→`Rows`/`Columns`/`Values`, `azureMap`→`Category`/`Size`.
  ⚠️ On `add visual`, **`-t` means `--title`, not `--type`** (the type is the positional arg).
- Place visuals at y ≥ 120 to avoid the default page title textbox.
- For each visual you add, check `../examples/visuals/default/<type>.json` first — fastest path to a working visual.
- **Long-named visual types** (`hundredPercentStackedAreaChart`, `hundredPercentStackedBarChart`, `hundredPercentStackedColumnChart`, `lineClusteredColumnComboChart`, `lineStackedColumnComboChart`) need explicit `--name "shortname"` — the auto-generated `<title>-<type>-<hash>` name overflows the PBIR schema length limit. Without `--name`, you get: `Schema validation failed for 'visual': name '…' is too long`.
