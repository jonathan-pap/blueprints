# SVG inside a table or matrix

The most common pattern. SVG renders per row.

## Procedure

1. Author the SVG measure — see `../per-chart/*` for ready-to-copy examples.
2. Set `dataCategory = ImageUrl` — see `../image-url-data-category.md`.
3. Add the measure to a `tableEx` or `pivotTable` `Values` role:

```bash
pbir visuals bind "<...>/MyTable.Visual" -a "Values:_Measures.Sparkline" -t Measure
```

4. In the visual JSON, find the values entry for the measure and set `imageHeight` and `imageWidth` to control rendered size (default uses the measure's intrinsic width / height):

```json
{
  "values": [
    {
      "displayName": "Sparkline",
      "imageHeight": 20,
      "imageWidth":  100
    }
  ]
}
```

## Sizing

- Sparklines: 100 × 20 typical.
- Data bars: cell-width × 16.
- Status pills: 60 × 20.
- Icons: 24 × 24.

Match `imageHeight` / `imageWidth` to the SVG's intrinsic `width` / `height` for crisp rendering.

## Limitation

No interactivity. SVG measures can't emit cross-filter events. For interactive in-cell visuals, use Deneb (`../../deneb/`).

## After

`../../../report/validate/validate.md`. Reopen Desktop.
