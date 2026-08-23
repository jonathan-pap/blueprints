# svg/per-chart — one file per DAX-SVG micro-chart

- `boxplot.md` — SVG — boxplot (per row): Quartiles + median + whiskers per row. Use for distribution comparison.
- `bullet.md` — SVG — bullet chart (per row): Actual vs target with banded ranges. Compact form of the classic Stephen Few bullet.
- `dumbbell.md` — SVG — dumbbell chart: Two dots connected by a line. Used for two-point comparisons (CY vs PY, before vs after, target vs actual).
- `html-item-card.md` — HTML-in-SVG — entity detail card: A "360" card for a single selected entity, composed with XHTML+CSS inside `<foreignObject>`. Reads the
- `html-market-board.md` — HTML-in-SVG — ranked board / listing: A leaderboard-style listing of TopN rows, composed with XHTML+CSS inside `<foreignObject>`. Reads the
- `ibcs-bar.md` — SVG — IBCS-styled bar: International Business Communication Standards bar pattern: actual vs prior, with variance bar overlay.
- `jitter-plot.md` — SVG — jitter plot (per row): Dots placed along a horizontal axis with vertical jitter to show distribution density per row.
- `lollipop.md` — SVG — lollipop chart: A line + dot pattern, often used as a less heavy alternative to bar charts.
- `overlapping-bars-with-variance.md` — SVG — overlapping bars with variance: Like `overlapping-bars.md` but adds a colored overlay on the variance region — same idea as `ibcs-bar.md` with…
- `overlapping-bars.md` — SVG — overlapping bars: Two bars overlaid: prior in light, actual in dark on top. Use when comparing two periods in-row.
- `progress-bar.md` — SVG — progress bar: Percent-of-goal as a horizontal bar.
- `sparkline.md` — SVG — sparkline (per row in a table): Mini trend line per row. Showing direction at a glance.
- `status-pill.md` — SVG — status pill: Colored rounded-rect with a text label. Best for status indicators ("Active", "Late", "On Track").
- `target-bar.md` — SVG — target bar (linear gauge): A horizontal track split into red / amber / green zones with a needle marking where a 0–1
- `waterfall.md` — SVG — waterfall (per row): Stepped bars showing positive/negative contributions to a total. Compact form for in-table use.
