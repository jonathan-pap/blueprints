# Add a gauge

Half-circle showing actual against min/max bounds. Use sparingly — KPI cards (`kpi-card.md`) usually communicate the same information with less ink.

## Create

```bash
pbir add visual gauge "<project>.Report/Overview.Page" --title "Capacity Utilization" \
  --x 24 --y 300 --width 300 --height 200
```

## Bind fields

```bash
pbir visuals bind "<...>/Capacity Utilization.Visual" \
  -a "Y:Operations.Utilization"          -t Measure \
  -a "TargetValue:Operations.Target"     -t Measure \
  -a "MinValue:Operations.Min Capacity"  -t Measure \
  -a "MaxValue:Operations.Max Capacity"  -t Measure
```

## Field roles

- `Y` (Measure, required) — the actual reading
- `TargetValue` (Measure) — optional target indicator line
- `MinValue`, `MaxValue` (Measure) — bound the dial

Confirm with `pbir visuals bind "<...>" --list-roles` if uncertain.

## When to use

- Capacity / utilization metrics where the bounds matter (0%–100%, 0–max).
- Single-value indicators where the dial form adds meaning vs a number.

## When NOT to use

- Comparing multiple metrics → use multiple `kpi-card.md` instances.
- The bounds are unclear → KPI card with target is cleaner.

## Templates

- `../examples/visuals/default/gauge.json`
- `../examples/visuals/formatted/gauge.json`

## After

`../validate/validate.md`.
