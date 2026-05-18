# Engine — R visuals (ggplot2)

> Static PNG charts rendered server-side from an R script. Best where R's ecosystem excels: forecast plots, pheatmap, corrplot, ggplot2 statistical visualisations.

## When to use R visuals

- Forecast / time-series / statistical chart not available natively or in Deneb.
- R libraries are the tool of choice (forecast, pheatmap, corrplot, lattice, ggpubr).
- The team already has R fluency.

## When NOT to use R visuals

- Need interactivity → use `../deneb/`.
- Need an inline graphic in a table → use `../svg/`.
- Python ecosystem fits better → use `../python/`.

## Workflow router

- **One-time: enable R in PBI Desktop** → `setup.md`
- **How the `dataset` data.frame is built** → `bind-dataset.md`
- **Common pitfalls** (libraries, randomness, output capture) → `common-pitfalls.md`
- **Per chart type** → `charts/_index.md` for bar / trend-line / bullet / ytd-line
- **Inspiration** → `community-examples.md`

## Examples

Scripts (paste into the R visual's code editor):

- `examples/script/bar-chart.R`
- `examples/script/trend-line.R`

Full visual JSON (drop into `<project>.Report/definition/pages/<page>/visuals/`):

- `examples/visual/bar-chart.json`
- `examples/visual/bullet-chart.json`
- `examples/visual/trend-line.json`
- `examples/visual/ytd-line-chart.json`

## Rules

- Use only packages installed in the Power BI R env — missing libraries break the visual silently.
- Cap data points: R visuals re-render on every filter change and have a 150 k row default limit.
- Output a single plot — `print(p)` once at the end.
- Avoid randomness without `set.seed()` — snapshot will differ each refresh.
- Use a hardcoded palette synced to `../../theme/` rather than ggplot2 defaults.

## Before showing to the user

Run `../../../04-review/reviewers/r-review.md` — 7-point validation checklist.
