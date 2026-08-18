# Audit - telecom-churn report

Generated 2026-08-18 - theme `Retention Signal (Light)`, page 1280x720, 12-col x 12-row grid.

## Quick checks

| Page | Visuals | Data visuals | Slicers | Verdict |
|---|---|---|---|---|
| AtRisk | 15 | 7 | 3 | optimal |
| Drivers | 19 | 10 | 3 | acceptable |
| Overview | 22 | 10 | 3 | acceptable |
| Profile | 13 | 6 | 3 | optimal |
| ttAttr | 6 | 5 | 0 | optimal |
| ttCustomer | 6 | 6 | 0 | optimal |
| ttReason | 6 | 5 | 0 | optimal |
| ttSegment | 6 | 5 | 0 | optimal |

Data visuals total: **54** across 8 pages. Decorative (textbox/image/shape) are excluded - they carry no query cost.

Custom theme applied: **Spectrum-Light-v1.3.json**

## Design-system compliance

- Off-snap coordinates (not a multiple of 8): **0**
- Off-grid origins (not on or near a region edge): **0** _(4 tooltip pages excluded - 320x240 popups, not on the 12x12 grid)_

`resolve_layout.py` snaps region EDGES, but a helper that insets a region (heading strip + gap) can still land content off-snap - this check found 44 such coordinates on its first run, from a 6px gap. It is not redundant with the resolver.

## Theme compliance

- Hex values outside the documented palette: **0**
  - none. Colours in visual.json are all palette members; SVG measures reference the `[Clr *]` measures rather than inline hex, so a re-theme reaches them.

