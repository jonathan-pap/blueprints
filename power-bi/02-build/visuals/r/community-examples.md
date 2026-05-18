# R visual — inspiration

- **R Graph Gallery** — https://r-graph-gallery.com/ (definitive ggplot2 + base R catalogue)
- **ggplot2 reference** — https://ggplot2.tidyverse.org/reference/
- **tidyverse blog** — https://www.tidyverse.org/blog/
- **`patchwork` for multi-panel** — https://patchwork.data-imaginist.com/
- **`gghighlight` for emphasized series** — https://yutannihilation.github.io/gghighlight/
- **Power BI Community** — search "R visual"

## When to browse

- Need a chart not in the catalogue → R Graph Gallery first.
- Need statistical / scientific visuals (forecast, heatmap, corrplot, pheatmap) → R-specific packages excel here.
- Need polished multi-panel layouts → `patchwork`.

## Adapt rules

External examples come with their own data frames. Always:

1. Rewrite to read from `dataset`.
2. Rename example fields → your bound names.
3. Replace example palettes with theme-matching hex.
4. Wrap final plot in `print(p)`.

## Save useful patterns

Drop scripts into `../../examples/script/<name>.R`. Add wrapper file under `charts/<name>.md`. Update `_index.md`.
