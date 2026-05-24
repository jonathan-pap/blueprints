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
