# svg/ — atomic files

> Inline SVG via DAX extension measures. No custom visual install. Rendered as `ImageUrl` in table/matrix/card.

## Foundations

- `data-uri-format.md` — the `data:image/svg+xml;utf8,...` string + escaping
- `image-url-data-category.md` — the `dataCategory = ImageUrl` requirement
- `theme-color-references.md` — pull colors from theme rather than hardcoding

## Wiring (where the SVG renders)

- `wiring/in-table-matrix.md` — most common; column in `tableEx` / `pivotTable`
- `wiring/in-card.md` — full-card SVG (`cardVisual` with image binding)
- `wiring/in-slicer.md` — SVG inside a slicer button

## Per chart type (each maps to an `examples/*.dax` file)

- `per-chart/sparkline.md`
- `per-chart/progress-bar.md`
- `per-chart/bullet.md`
- `per-chart/status-pill.md`
- `per-chart/lollipop.md`
- `per-chart/ibcs-bar.md`
- `per-chart/overlapping-bars.md`
- `per-chart/overlapping-bars-with-variance.md`
- `per-chart/dumbbell.md`
- `per-chart/waterfall.md`
- `per-chart/boxplot.md`
- `per-chart/jitter-plot.md`

## Reference

- `community-examples.md` — gallery / inspiration
