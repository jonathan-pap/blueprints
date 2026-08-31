# Size a visual

Set width, height of an existing visual.

> **The 12×12 grid is the default — these pixel numbers are its output, not your input.**
> Resolve the visual's span from `defaults.<type>` in the project's `design-system.yaml` first
> ([design-system.md](design-system.md)), then pass the resolved numbers below.
> Choosing dimensions yourself is an **override**: do it only when the brief asks for that specific
> visual or it's a genuine one-off, and record it in the yaml `overrides:` block with a reason.
> Unrecorded off-token sizes are flagged by
> [`audit-layout-consistency.sh`](../../../04-review/hooks/audit-layout-consistency.sh).

## CLI

```bash
pbir visuals size "<...>/Visual.Visual" --width 400 --height 160
```

## Recommended ranges

Fallback only — for a project with no `design-system.yaml` yet. Once the yaml exists its spans win;
if you find yourself reaching for these repeatedly, add a `defaults.<type>` entry instead.

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
