# P5 — Dual-axis plumbing

The combo-chart wiring that makes the column scale (currency/count) and the cumulative scale
(0–100%) coexist and read cleanly. None of it is conceptually deep — but skip it and the
cumulative line auto-scales to its own max, the "100%" never lines up with the top, and the
80% split looks arbitrary.

## Fix the secondary axis to 0–100%

```json
"valueAxis": [
  {
    "properties": {
      "secStart":    { "expr": { "Literal": { "Value": "0D" } } },
      "secEnd":      { "expr": { "Literal": { "Value": "1D" } } },
      "secTitleText":{ "expr": { "Literal": { "Value": "'Pareto'" } } },
      "alignZeros":  { "expr": { "Literal": { "Value": "false" } } },
      "fontSize":    { "expr": { "Literal": { "Value": "8D" } } }
    }
  }
]
```

`secStart 0` / `secEnd 1` pin the line axis to 0–100% (the share is a 0–1 fraction). Without
it the line fills the plot regardless of where 80% actually is, and the green/red split
loses meaning. `alignZeros: false` lets the two axes scale independently.

## Percent format on the cumulative

Set on the P3 projection itself (`"format": "0%;-0%;0%"`) — see
[sort-independent-cumulative.md](sort-independent-cumulative.md). That's what makes the line's
labels and axis read `80%`, not `0.8`.

## Per-bar selector (recap)

Every conditional bar property from [P4](threshold-split-emphasis.md) — fill and label tint —
needs the per-point selector or it won't vary across bars:

```json
"selector": { "data": [ { "dataViewWildcard": { "matchingOption": 1 } } ] }
```

## Line vs. marker styling

The split lines and the marker line are styled by `metadata` selector in
`objects.lineStyles` / `objects.markers`:

- `select2` (`Easy Pareto`) — markers on, stroke off → carries the dots + data labels.
- `select3` (`GreenLine`) — teal stroke + larger markers → the vital-few segment.
- `select4` (`RedLine`) — red stroke/markers → the trivial-many segment.

The exact transparency/marker-size literals are cosmetic; the load-bearing parts are *which
series shows a stroke* and *which carries the labels*. The template ships sensible values.

## Tidy-ups

- `legend.show: false` — color is self-explanatory; a legend of `GreenLine`/`RedLine`/`Pareto` is noise.
- `dataPoint[0].transparency` (~74) softens the columns so the line reads on top.
- Bar data labels at `InsideBase`, line labels `Above` — keeps the two from colliding.

## Rules

- **Always fix `secStart`/`secEnd` to 0/1.** This is the single most common reason a Pareto
  "looks off" — an auto-scaled secondary axis.
- Keep `categoryAxis.innerPadding` modest so bars stay adjacent (a Pareto reads as a solid
  descending block, not spaced bars).

## Done

Back to [workflow.md](../workflow.md) for validation, or pick a [variant](../variants/).
