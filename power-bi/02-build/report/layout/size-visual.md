# Size a visual

Set width, height of an existing visual.

## CLI

```bash
pbir visuals size "<...>/Visual.Visual" --width 400 --height 160
```

## Recommended ranges

- KPI / card: 200–300 × 130–160 (height ≥ 130 to prevent value clipping)
- Chart (small pair): 400 × 300
- Chart (medium): 600 × 400
- Full-width chart: page-width − 48 × 400
- Table / matrix: usually full-width × 300–500
- Slicer (horizontal): 200–400 × 56–80
- Slicer (vertical): 150–200 × 200–400

## Order matters when shrinking

Set `width`/`height` BEFORE `x`/`y` if the move would cross the page edge. Otherwise the intermediate state fails validation.

## See also

- `position-visual.md`
- `align-visuals-row.md` — calculates sizes that share equal gaps
