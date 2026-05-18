# R visual pitfalls

## 1. Missing package = silent failure

Library not in Power BI's R env → "R script returned no images" with no detail.

Fix: install via the exact R install Desktop uses. Verify with `.libPaths()` then `library(<name>)` in that env.

## 2. Randomness without a seed

Power BI re-runs the script on every filter change. Without `set.seed(42)`, the visual shifts each interaction.

Fix: always seed RNG.

## 3. Plot capture

Base R `plot()` calls and ggplot2 `ggplot(...)` both work, but the LAST one rendered is captured. Multiple `print()` calls drop earlier ones.

Fix: build one final plot. For multi-panel, use `gridExtra::grid.arrange()` or `patchwork::wrap_plots()` into a single object.

## 4. ggplot needs explicit print in script context

In an interactive R session, typing `ggplot(...) + geom_bar()` auto-prints. In Power BI's script context, it doesn't. Wrap in `print()`:

```r
p <- ggplot(dataset, aes(x = Region, y = Revenue)) + geom_col()
print(p)
```

## 5. Theme colors

R visuals don't read Power BI theme. Hardcode palette to match theme manually.

## 6. 150k row default

Above 150k rows, sampling kicks in. Non-deterministic.

## 7. Slow on filter

Full script re-runs per filter change. Avoid heavy computation; pre-aggregate where possible.

## 8. No interactivity

PNG output only. No cross-filter, no hover, no click. For interactivity → Deneb.
