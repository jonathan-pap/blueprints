# Layout guidelines — sizes, spacing math, z-order

> The numbers behind a clean page. *Where* things go is the detail gradient
> ([detail-gradient.md](detail-gradient.md)); this file is the dimensions, the equal-gap math, and the alignment
> rules that make a page read as deliberate rather than sloppy.

## Page dimensions

| Type | W × H | Use |
|---|---|---|
| Standard 16:9 | 1280 × 720 | Desktop default |
| Full HD | 1920 × 1080 | high-res / presentation |
| Letter | 816 × 1056 | print, portrait |
| 4:3 | 1280 × 960 | legacy |

Query before placing — never assume → [page-dimensions.md](page-dimensions.md).

## Margins, gaps, grid

- Page margins: 24–32px, **equal on all four edges**.
- Gap between visuals: 16px minimum, 24px recommended — **equal everywhere** (horizontal set equal; vertical set equal).
- Snap to an 8px/16px grid: positions 0,16,32,48… ; sizes 200,300,400…

## Whitespace tiers

Pick **one** tier for intra-group spacing and **one** for inter-group; never mix three spacing values in a single row.

| Tier | px | Use |
|---|---|---|
| Tight | 16 | between visuals in the same group (proximity = "these belong together") |
| Normal | 24 | between groups + page edge margins |
| Section | 32 | between major sections (header/body) |

Proximity is grouping: ≤16px apart reads as one group; ≥32px apart reads as separate — cheaper and cleaner than boxes/borders.

## Reading patterns (where the eye lands)

| Pattern | Path | Use for | Archetype |
|---|---|---|---|
| **F** | left-anchored, top-heavy scan | dense analytical/operational pages, tables, filter rails | Analytical, Operational |
| **Z** | top-left → top-right → bottom-left → bottom-right | sparse executive/narrative pages: headline + hero + a few supports | Executive, Narrative |

**Top-left carries the heaviest message** — put the insight title, primary KPI, or hero there. Set each visual's `tabOrder` to match the reading order (accessibility).

## Slicer placement by count

| Slicers | Placement | Width impact |
|---|---|---|
| **1–3** | inline, right of the title row (~10–12% page width each) | none — cards/charts keep full content width |
| **4+** | vertical filter rail (≈2 grid columns: ~206px on 1280, ~310px on FHD) | F-pattern; content takes the remaining width |

A vertical rail is only justified when the slicers fill **≥50%** of the rail height — three dropdowns leave a dead column, so keep them inline. Reserve the title/slicer band first; **no data visual starts under a slicer** (z-order can't fix a bad layout).

## Zones (detail gradient)

| Zone | Purpose | Height | Visual types |
|---|---|---|---|
| 1 Summary | top | 150–200px | cards, KPIs, slicers |
| 2 Analysis | middle | 350–450px | charts, maps, gauges |
| 3 Detail | bottom | 350–450px | tables, matrices |

## Common visual sizes

- Cards/KPIs: 200–300 × 100–150
- Charts: small 400×300 · medium 600×400 · large 900×500
- Tables: variable width × 300–500
- Slicers: horizontal 200–400 × 60–80 · vertical 150–200 × 200–400

## Symmetrical spacing (critical)

Unequal gaps create visual tension even when nothing overlaps — one of the most common mistakes.
For a row of equal visuals:

```text
content_width = page_width − 2·margin
visual_width  = (content_width − gap·(n−1)) / n

# 4 visuals, 1280 page, 24 margin, 16 gap:
content = 1280 − 48 = 1232 ; widths = (1232 − 48)/4 = 296 ; x = 24, 336, 648, 960
```

For mixed-width visuals sharing a row, the gap between each adjacent pair must still match:
verify `B.x − (A.x + A.width)` is identical for all pairs. A 4–8px discrepancy already looks off.

## Vertical column alignment across rows (critical)

When rows share a vertical split, the gutter must line up top-to-bottom even if the visuals
differ in type/size:

```text
WRONG                                  RIGHT
[--- 648 ---][16][--- 584 ---] row1    [--- 648 ---][16][--- 584 ---] row1
[--- 632 ----][16][-- 600 --] row2     [--- 648 ---][16][--- 584 ---] row2
             ^ gutters don't align                  ^ same column edge
```

Keep the split x identical across rows (e.g. A ends at 648, B starts at 664 → C ends at 648, D
starts at 664); the widths of C/D may differ but the gutter is continuous.

## Z-order bands

- Base visuals: `z` 0–999
- Overlays / highlights: 1000–1999
- Tooltips / popups: 2000+

## Visual-count vs performance

| Count | Status |
|---|---|
| 6–8 | optimal |
| 9–12 | slight impact |
| 13–15 | noticeable delay |
| 16+ | performance issues |

Textboxes, images, shapes, and buttons are cheap — they don't count against this much.

## Related

- [detail-gradient.md](detail-gradient.md) — 3-30-300 (what goes where)
- [align-visuals-row.md](align-visuals-row.md) · [align-visuals-grid.md](align-visuals-grid.md) — equal-gap placement commands
- [../references/cards-and-kpis.md](../references/cards-and-kpis.md) · [../references/tables-and-matrices.md](../references/tables-and-matrices.md) — per-zone design
