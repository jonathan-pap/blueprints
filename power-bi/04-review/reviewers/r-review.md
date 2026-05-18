# R visual review checklist

Run after writing or modifying an R visual script, before showing to the user.

## Validation (pass / fail each)

1. **`print(p)` present** — ggplot2 objects require explicit printing. Must be the final call.
2. **`dataset` not created** — The data.frame is auto-injected by Power BI. Script must not define it.
3. **Column access** — Index-based (`dataset[,1]`) preferred to avoid name escaping. Backticks for names with spaces: `` dataset$`Order Lines` ``.
4. **Supported packages only** — ggplot2, dplyr, tidyr, ggrepel, patchwork, cowplot, corrplot, viridis, RColorBrewer, forecast, pheatmap, treemap, lattice. **No networking-dependent packages.**
5. **No networking** — Zero URL fetches or web requests.
6. **Empty-data guard** — Handles `nrow(dataset) == 0` gracefully.
7. **Single output** — Only one plot renders per visual.

## Design feedback (≤ 3 suggestions max)

- ggplot2 preferred over base R graphics?
- `theme_minimal()` or similar clean theme applied?
- Colors hex-coded and muted (not ggplot2 defaults)?
- Factor levels set explicitly for sort order?
- Margins adequate (`plot.margin`) to prevent clipping?

## Verdict

`READY` (all 7 pass) — show to user.
`NEEDS CHANGES` (any fail) — list failures + fixes, do not show until corrected.

## Source / see also

- Pattern source: upstream `_examples/reports/agents/r-reviewer.agent.md`
- Authoring guides: `../../02-build/visuals/r/`
