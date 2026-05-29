# Foundation — HTML in SVG (`<foreignObject>`)

> The escape hatch from raw SVG primitives. An `ImageUrl` SVG measure can embed a `<foreignObject>`
> holding real **XHTML + CSS** — so you compose layouts from DAX with flexbox/grid, **text that
> wraps**, **inline mixed styling** (a colored bold number mid-sentence), CSS counters/lists, and
> **chips that wrap** — none of which raw `<text>`/`<rect>` can do. Same engine as the rest of
> `svg/` (data URI + `dataCategory = ImageUrl`), no custom-visual install.

## The shape

```
data:image/svg+xml;utf8,
<svg xmlns='http://www.w3.org/2000/svg' width='440' height='380'>
  <foreignObject x='0' y='0' width='440' height='380'>
    <div xmlns='http://www.w3.org/1999/xhtml' class='c'> … XHTML + CSS … </div>
  </foreignObject>
</svg>
```

Required:
- `xmlns` on the `<svg>` **and** on the inner `<div>` (the XHTML namespace) — miss either → broken image.
- `width`/`height` on both `<svg>` and `<foreignObject>` — the foreignObject **clips** at its height, so size for the worst case (max rows) or content gets cut.

## Escaping & well-formedness (stricter than HTML)

`<foreignObject>` content is **XHTML**, not loose HTML — it must be well-formed or the whole image fails silently:

- **Use single-quoted attributes** (`class='c'`, `style='...'`). Avoids the `""`-doubling pain that dense CSS would cause in DAX (see `data-uri-format.md`). Single quotes need no DAX escaping.
- **Self-close void tags:** `<br/>`, `<img .../>`, `<hr/>` — never bare `<br>`.
- **Escape `&` → `&amp;`** in any data text: `SUBSTITUTE ( [Name], "&", "&amp;" )`. Unescaped `&` breaks parsing.
- **Symbols via numeric entities:** `&#215;` (×), `&#183;` (·), `&#9650;` (▲), `&#9660;` (▼), `&#9679;` (●). Safer than literal glyphs.
- **32 KB measure-string ceiling** — rich cards eat budget fast; keep one component per measure and cap row counts.

## Styling: inline vs `<style>` block

Both work in Power BI's Chromium webview. A `<style>` block with classes keeps repeated row/tile CSS out of the per-row string (much smaller); use **inline `style='...'`** only for the dynamic bits (a rarity color, a bar width). The component examples do exactly this.

## Animation & interactivity — know the hard line

Power BI renders the SVG as an **`<img>`** (a replaced element). That decides everything:

| Want | Works? | Do it with |
|---|---|---|
| Pulse / spin / shimmer / fly-in (declarative loops) | ✅ | SMIL `<animate>` / `<animateTransform>`, or CSS `@keyframes` |
| Mouse **hover / click / drilldown** on the image | ❌ | Native **Button** states (Default/Hover/Press) — `../../report/...`; or the **HTML Content** custom visual for a live DOM |

Declarative-animation caveats: it **replays on every measure re-evaluation** (any slicer/cross-filter restarts it — invisible for infinite loops, jarring for one-shot fly-ins), and **does not animate in PDF/PowerPoint export**. SMIL is more reliable than CSS-in-foreignObject for animation.

Pulsing "live" dot (pure SVG SMIL — no foreignObject needed):

```dax
"<circle cx='16' cy='20' r='6' fill='#2ecc71'>" &
  "<animate attributeName='r' values='5;7;5' dur='1.4s' repeatCount='indefinite'/>" &
  "<animate attributeName='opacity' values='1;0.5;1' dur='1.4s' repeatCount='indefinite'/>" &
"</circle>"
```

Spinner (rotate): `<animateTransform attributeName='transform' type='rotate' from='0 24 24' to='360 24 24' dur='0.9s' repeatCount='indefinite'/>` on a `<path>`.

## When to use vs not

**Use** for rich text/layout components: entity "360" cards, narrative insight cards (inline-colored numbers), ranked boards/leaderboards, activity feeds/timelines, chip/tag clouds (flex-wrap), rich matrix cells.

**Don't use** when: the page is **exported to PDF/PPT** (renders blank); you need **interactivity** (inert image — use buttons / HTML visual); the data is **large** (you marshal rows through `CONCATENATEX` — great for ~5–30 rows, bad for thousands).

## Components built on this foundation

- `per-chart/html-item-card.md` — entity "360" card (rarity color, stat grid, ingredient chips, craft-vs-buy verdict). Example: `examples/html-item-card-measure.dax`.
- `per-chart/html-market-board.md` — ranked listing board (TopN rows, value bars). Example: `examples/html-market-board-measure.dax`.

For an interactive **"show N"** picker feeding a board/list, harvest a disconnected slicer → see the disconnected-selection recipe (`../../recipes/disconnected-selection-emphasis/`).

## Wire & validate

Renders like any SVG measure — `dataCategory = ImageUrl`, dropped in a `tableEx` cell sized to the component (see `wiring/in-table-matrix.md`). Run the SVG reviewer (`../../../04-review/reviewers/svg-review.md`) before shipping, plus the two extra checks: **no export dependency**, **well-formed XHTML**.
