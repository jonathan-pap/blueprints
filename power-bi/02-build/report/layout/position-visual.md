# Position a visual

Set x, y of an existing visual.

> **The 12×12 grid is the default — these pixel numbers are its output, not your input.**
> Resolve the visual's region from the project's `design-system.yaml` first
> ([design-system.md](design-system.md)), then pass the resolved numbers below.
> Choosing coordinates yourself is an **override**: do it only when the brief asks for that specific
> visual or it's a genuine one-off, and record it in the yaml `overrides:` block with a reason.
> Unrecorded off-grid positions are flagged by
> [`audit-layout-consistency.sh`](../../../04-review/hooks/audit-layout-consistency.sh).

## CLI

```bash
pbir visuals position "<...>/Visual.Visual" --x 24 --y 120
```

## Rules

- Top-left corner = (24, 24) by convention (24 px margin) — this is `grid.margin` in the yaml, not a number to retype.
- Avoid y < 120 unless you've removed the default page-title textbox.
- Never overlap another visual. Run `inspect-bindings.md` from `../bind/` to see current positions, or `pbir tree "<project>.Report" -v`.

## See also

- `size-visual.md` — set dimensions
- `align-visuals-row.md` — equal-gap row
- `page-dimensions.md` — confirm page bounds first
