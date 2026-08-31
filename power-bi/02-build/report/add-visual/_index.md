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

**Rule: always verify field names first.** Open `../bind/find-canonical-name.md` before creating any data visual — copy the exact `Table.Field` name from the model (e.g., `FactQuests.BountyAmount`). Never guess from English labels; a visual bound to a wrong field will render data incorrectly and fail validation. Verify your field names are real before any CLI call.

**Rule: bind each role to one field.** Each chart type has roles (e.g., a bar chart has `Category` and `Y`; a scatter has `X`, `Y`). Bind each role to the correct field from the model. Inline binding — adding the bindings in the same call as the visual creation — is preferred (one command, one edit to PBIR). The `pbir` CLI lets you use `-d "Role:Table.Field"` (repeatable for multiple roles); separate binding is a second step, also valid but less efficient.

**Rule: validate after each visual.** Open `../validate/validate.md` after adding or changing each visual — the `pbir` CLI enforces schema correctness, but catching issues visual-by-visual keeps the PBIR file honest.

**Rule: the 12×12 grid decides size and position — the default, every time.** Read `projects/<name>/design-system.yaml` and resolve the visual's span (size) and region (placement) to pixels before you write the `--x/--y/--width/--height` flags; the numbers in the examples below are illustrative output, not values to copy. Place each visual at or below y=120 (the default page title textbox). Hand-picking dimensions is an **override** — allowed only when the brief asks for that specific visual or it's a genuine one-off, and it must be recorded in the yaml `overrides:` block with a reason. Off-grid, off-token, or overlapping visuals fail the layout audit ([`../layout/design-system.md`](../layout/design-system.md)).

**Rule: start from a template.** Check `../examples/visuals/default/<type>.json` for your chart type — it has the schema structure already correct and ready to bind. Faster than hand-editing.

**Rule: short names for long types.** Visual type names like `hundredPercentStackedAreaChart` or `lineClusteredColumnComboChart` are long; the auto-generated name (`<title>-<type>-<hash>`) can overflow PBIR's length limit. Provide an explicit short name (e.g., `--name "sales-trend"`); without it you'll see: `Schema validation failed for 'visual': name '…' is too long`.

### Tool reference (pbir CLI syntax)

- **List available roles for a visual type:** `pbir add visual --list <visualType>` shows role names (e.g., `cardVisual`→`Data`; charts→`Category`/`Y`/`Y2`; `scatterChart`→`X`/`Y`; `gauge`→`Y`/`TargetValue`; `tableEx`/`slicer`→`Values`; `pivotTable`→`Rows`/`Columns`/`Values`; `azureMap`→`Category`/`Size`).
- **Add a visual with bindings:** `pbir add visual <pageName> <visualType> -d "Role1:Table.Field1" -d "Role2:Table.Field2"` (repeatable `-d` for each role).
- **Note:** `-t` means `--title`, not `--type` (the type is the positional argument).
