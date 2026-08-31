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

**Rule: validate the page, not each visual.** `pbir validate` is whole-report only (~2s), so running it per visual re-checks the entire report to verify one addition — and each file write is already schema-checked automatically by the `validate-pbir.sh` hook. Validate immediately only when the risk is real: a hand-edited JSON, a visual type you haven't used before, an unfamiliar property. Otherwise validate once the page is complete, together with the trap lint that catches what schema validation can't ([`../validate/validate.md`](../validate/validate.md)).

**Rule: the 12×12 grid decides size and position — the default, every time.** Read `projects/<name>/design-system.yaml` and resolve the visual's span (size) and region (placement) to pixels before you write the `--x/--y/--width/--height` flags; the numbers in the examples below are illustrative output, not values to copy. Place each visual at or below y=120 (the default page title textbox). Hand-picking dimensions is an **override** — allowed only when the brief asks for that specific visual or it's a genuine one-off, and it must be recorded in the yaml `overrides:` block with a reason. Off-grid, off-token, or overlapping visuals fail the layout audit ([`../layout/design-system.md`](../layout/design-system.md)).

**Rule: the template is the shape; the CLI is one way to apply it.** Start from `../examples/visuals/default/<type>.json` (bare) or `formatted/<type>.json` (styled) — the schema structure is already correct, and the JSON is the durable artifact. `pbir add visual` is a convenient applier, not the definition: it's a community tool, and anything its flags can't reach (conditional formatting, `goals.goalText`, nested objects) is edited in the JSON anyway. Writing the file directly, or via [`../tools/pbirkit.py`](../tools/pbirkit.py), is equally valid. Full catalogue: [`../examples/visuals/__index.md`](../examples/visuals/__index.md); why this matters: [`../../../file-map.md`](../../../file-map.md).

**Rule: short names for long types.** Visual type names like `hundredPercentStackedAreaChart` or `lineClusteredColumnComboChart` are long; the auto-generated name (`<title>-<type>-<hash>`) can overflow PBIR's length limit. Provide an explicit short name (e.g., `--name "sales-trend"`); without it you'll see: `Schema validation failed for 'visual': name '…' is too long`.

### Tool reference (pbir CLI syntax)

- **List available roles for a visual type:** `pbir add visual --list <visualType>` shows role names (e.g., `cardVisual`→`Data`; charts→`Category`/`Y`/`Y2`; `scatterChart`→`X`/`Y`; `gauge`→`Y`/`TargetValue`; `tableEx`/`slicer`→`Values`; `pivotTable`→`Rows`/`Columns`/`Values`; `azureMap`→`Category`/`Size`).
- **Add a visual with bindings:** `pbir add visual <pageName> <visualType> -d "Role1:Table.Field1" -d "Role2:Table.Field2"` (repeatable `-d` for each role).
- **Note:** `-t` means `--title`, not `--type` (the type is the positional argument).
