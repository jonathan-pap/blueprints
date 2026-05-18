# Equal-gap row of visuals

Lay out N visuals horizontally with identical gaps and equal widths. The single most-visible quality signal in a report.

## Formula

```
content_width = page_width - (2 * margin)
total_gaps    = gap * (n - 1)
visual_width  = (content_width - total_gaps) / n
x[i]          = margin + i * (visual_width + gap)
```

## Worked example

4 KPI cards on a 1280 × 720 page, margin 24, gap 16:

```
content_width = 1280 - 48 = 1232
total_gaps    = 16 * 3   = 48
visual_width  = (1232 - 48) / 4 = 296
x positions:   24, 336, 648, 960
```

Commands:

```bash
pbir add visual cardVisual "<...>/Overview.Page" --title "Revenue"   --x 24  --y 120 --width 296 --height 140
pbir add visual cardVisual "<...>/Overview.Page" --title "Orders"    --x 336 --y 120 --width 296 --height 140
pbir add visual cardVisual "<...>/Overview.Page" --title "Margin"    --x 648 --y 120 --width 296 --height 140
pbir add visual cardVisual "<...>/Overview.Page" --title "Customers" --x 960 --y 120 --width 296 --height 140
```

## Verify

```bash
pbir tree "<project>.Report" -v   # confirm all x positions form the expected arithmetic sequence
```

## After

`../validate/validate.md`.
