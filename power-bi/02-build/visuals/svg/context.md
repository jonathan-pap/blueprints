# Engine — SVG (via DAX measure)

> Inline SVG graphics rendered as ImageUrl in table/matrix/card visuals. No custom visual install. Best for compact, in-context graphics: sparklines, data bars, status pills, progress bars, bullet/lollipop micro-charts.

## When to use SVG

- Need a graphic *inside* a table or matrix row.
- Need a sparkline / mini-trend per row.
- Need a status indicator (pill, traffic light, arrow) driven by DAX.
- Want zero custom-visual install/footprint.

## When NOT to use SVG

- Need interactivity / cross-filter → use `../deneb/`.
- Need a full statistical visualization → use `../python/` or `../r/`.
- Need a standalone large chart → SVG works but Deneb is usually cleaner.

## How it works

1. Write a DAX measure that returns a string of the form `"data:image/svg+xml;utf8,<svg ...>...</svg>"`.
2. Set the measure's **`dataCategory = ImageUrl`** in TMDL (see `../../model/object-types/column-properties.md`).
3. Bind the measure to a visual role that accepts an image (table/matrix `Values`, card `Image URL`).

Power BI renders the returned string as an inline SVG. No CSS, no JS, no animation.

## Workflow router

- **Data URI shape + escaping** → `data-uri-format.md`
- **SVG element cheat-sheet** → `svg-elements.md`
- **The `dataCategory = ImageUrl` requirement** → `image-url-data-category.md`
- **Theme-color integration** → `theme-color-references.md`
- **Wire into a table / matrix** → `wiring/in-table-matrix.md`
- **Wire as a full card** → `wiring/in-card.md`
- **Wire into a slicer button** → `wiring/in-slicer.md`
- **Wire as a standalone image visual** → `wiring/in-image.md` (KPI header, dashboard tile, wide gauge)
- **Per chart type** → `per-chart/_index.md` for sparkline / progress-bar / bullet / status-pill / lollipop / ibcs-bar / overlapping-bars / dumbbell / waterfall / boxplot / jitter-plot / target-bar
- **Inspiration** → `community-examples.md`

## Example DAX measures (ready to copy)

Each `.dax` file in `examples/` is a complete measure — copy, rename, adjust field bindings.

- `examples/sparkline-measure.dax` — trend line per row
- `examples/progress-bar-measure.dax` — % of goal as a horizontal bar
- `examples/bullet-chart-measure.dax` — actual + target + range bands
- `examples/status-pill-measure.dax` — coloured pill driven by threshold
- `examples/lollipop-conditional-measure.dax` — lollipop with conditional colour
- `examples/ibcs-bar-measure.dax` — IBCS-styled bar with variance
- `examples/overlapping-bars-measure.dax` — actual vs prior overlapped
- `examples/overlapping-bars-with-variance-measure.dax` — + variance label
- `examples/dumbbell-chart-measure.dax` — two-point comparison per row
- `examples/boxplot-measure.dax` — mini boxplot per row
- `examples/jitter-plot-measure.dax` — mini jittered distribution
- `examples/waterfall-measure.dax` — waterfall steps per row
- `examples/target-bar-svg.dax` — linear gauge: red/amber/green zones + needle (card / image)

## Rules

- The returned string MUST start with `data:image/svg+xml;utf8,`.
- The measure MUST have `dataCategory = ImageUrl` — without it, Power BI shows the raw string.
- Escape inner double quotes by doubling them (`""`) inside DAX.
- Keep the SVG small: width × height suitable for a table cell (typical: 100 × 20 for sparklines, 24 × 24 for icons).
- Use theme sentiment colours (`good` / `bad` / `neutral`) returned from a sibling measure so re-theming propagates.

## Before showing to the user

Run `../../../04-review/reviewers/svg-review.md` — 10-point validation checklist.
