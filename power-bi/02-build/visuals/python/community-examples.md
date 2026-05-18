# Python visual — inspiration

- **matplotlib gallery** — https://matplotlib.org/stable/gallery/index.html
- **seaborn examples** — https://seaborn.pydata.org/examples/index.html
- **Python Graph Gallery** — https://python-graph-gallery.com/
- **Power BI Community** — search "Python visual"

## When to browse

- Need a chart type not in the catalogue → matplotlib or seaborn gallery first.
- Need stats-heavy visuals (distributions, regressions, residuals) → seaborn.
- Need polished statistical figures (heatmap, joint plot, pair plot) → seaborn defaults are quite good.

## Adapt rules

External examples assume their own DataFrame shape. Always:

1. Rewrite to read from `dataset`.
2. Map example column names → your bound field names.
3. Replace example palettes with theme-matching hex colors.
4. Add `plt.tight_layout()` so labels don't get cropped.

## Save useful patterns

Drop reusable scripts into `../../examples/script/<name>.py` and a wrapper file under `charts/<name>.md`. Update `_index.md`.
