# Engine — Python visuals (matplotlib / seaborn)

> Static PNG charts rendered server-side from a Python script. Best for statistical visualisations where Python's libraries excel.

## When to use Python visuals

- Distribution / regression / correlation plots that native Power BI cannot express well.
- The team already has matplotlib / seaborn fluency.
- The output value is the analysis, not the interaction.

## When NOT to use Python visuals

- Need cross-filter or hover interactivity → use `../deneb/`.
- Need an inline graphic in a table → use `../svg/`.
- Need a standard chart that native + theme could render → use `../../report/`.

## Workflow router

- **One-time: enable Python in PBI Desktop** → `setup.md`
- **How the `dataset` DataFrame is built** → `bind-dataset.md`
- **Common pitfalls** (libraries, randomness, output capture) → `common-pitfalls.md`
- **Per chart type** → `charts/_index.md` for bar / trend-line / kpi-card / ytd-line
- **Inspiration** → `community-examples.md`

## Examples

Scripts (paste into the Python visual's code editor):

- `examples/script/bar-chart.py`
- `examples/script/trend-line.py`

Full visual JSON (drop into `<project>.Report/definition/pages/<page>/visuals/`):

- `examples/visual/bar-chart.json`
- `examples/visual/kpi-card.json`
- `examples/visual/trend-line.json`
- `examples/visual/ytd-line-chart.json`

## Rules

- Use only packages installed in the Power BI Python env — missing imports break the visual silently.
- Cap data points: Python visuals re-render on every filter change and have a 150 k row default limit.
- Output a single figure — multiple `plt.show()` calls are ignored.
- Avoid randomness without a seed — snapshot will differ each refresh.
- Use theme colours via a hardcoded palette synced to `../../theme/` rather than matplotlib defaults.

## Before showing to the user

Run `../../../04-review/reviewers/python-review.md` — 8-point validation checklist.
