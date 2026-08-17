# layout/ — atomic files

- `design-contract.md` — the `Design Brief:` handoff schema (from [`../design/`](../references/design-identity.md)) — grid regions, bands, placements, space rules + the handoff validation checklist. The spec the steps below implement.
- `design-system.md` — **read first** — project layout tokens (`design-system.yaml`): the 12×12 grid, per-type spans, bands, gaps. The dimension counterpart to the theme.
- `design-system-default.yaml` — copyable starter tokens for a new project
- `page-dimensions.md` — query and choose page size
- `position-visual.md` — set x, y
- `size-visual.md` — set width, height
- `align-visuals-row.md` — equal-gap row of visuals
- `align-visuals-grid.md` — equal-gap grid
- `detail-gradient.md` — 3-30-300 layout pattern (where things go)
- `layout-guidelines.md` — page sizes, equal-gap math, cross-row column alignment, z-order, perf limits
- `visual-groups.md` — bind visuals to move/scale as one unit (`pbir visuals group`)
- `copy-move-delete.md` — rearrange visuals

## Golden rules

- Visuals must not overlap.
- All horizontal gaps on a page must be equal. Same for vertical gaps.
- All edge margins on a page must be equal.
- Query actual page dimensions before placing — never assume.
