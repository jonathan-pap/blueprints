# SVG inside a slicer

Slicer buttons can display SVG icons. Pair a status SVG measure with a slicer for visual selection (e.g., region cards as a slicer).

## Procedure

1. Author the SVG measure — see `../per-chart/status-pill.md` for the typical pattern.
2. Set `dataCategory = ImageUrl`.
3. Bind to the slicer's image role:

```bash
pbir add visual slicer "<project>.Report/Overview.Page" \
  --x 24 --y 120 --width 600 --height 80
pbir visuals bind "<...>/Slicer.Visual" \
  -a "Values:Geography.Region"       -t Column \
  -a "Image:_Measures.RegionStatus"  -t Measure
```

4. In the slicer's `visual.json` objects, enable image display (`buttonShape` settings; varies by slicer type).

## Notes

- Works best with `advancedSlicerVisual` (button-style slicers).
- Classic dropdown slicer ignores image role.
- The SVG must look good at 24–32 px height — that's the typical slicer-button thumbnail size.

## See also

- `../per-chart/status-pill.md` — typical icon shape for slicer buttons
- `../../../report/add-visual/slicer.md` — slicer basics
