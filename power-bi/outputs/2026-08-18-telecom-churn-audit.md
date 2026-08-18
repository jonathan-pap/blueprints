# Audit - telecom-churn report

Generated 2026-08-18 - theme `Retention Signal (Light)`, page 1280x720, 12-col x 12-row grid.

## Quick checks

| Page | Visuals | Data visuals | Slicers | Verdict |
|---|---|---|---|---|
| AtRisk | 9 | 4 | 0 | optimal |
| Drivers | 15 | 7 | 0 | optimal |
| Overview | 18 | 7 | 0 | optimal |
| Profile | 5 | 2 | 0 | optimal |

Data visuals total: **20** across 4 pages. Decorative (textbox/image/shape) are excluded - they carry no query cost.

Custom theme applied: **Spectrum-Light-v1.1.json**

## Design-system compliance

- Off-snap coordinates (not a multiple of 8): **0**
- Off-grid origins (not on or near a region edge): **0**

`resolve_layout.py` snaps region EDGES, but a helper that insets a region (heading strip + gap) can still land content off-snap - this check found 44 such coordinates on its first run, from a 6px gap. It is not redundant with the resolver.

## Theme compliance

- Hex values outside the documented palette: **0**
  - none. Colours in visual.json are all palette members; SVG measures reference the `[Clr *]` measures rather than inline hex, so a re-theme reaches them.

