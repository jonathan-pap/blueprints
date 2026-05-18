# Deneb — KPI card

Full custom KPI with headline value, target indicator, sparkline, and arrow icon — all in one Vega spec.

Use Deneb KPI when native `kpi` visual is too rigid (e.g. need a specific icon style, custom typography, layered annotations). Otherwise use `../../report/add-visual/kpi-card.md`.

## Bindings

```bash
pbir visuals bind "<...>/MyKpi.Visual" \
  -a "Actual:Sales.Revenue"       -t Measure \
  -a "Target:Sales.Revenue 1YP"   -t Measure \
  -a "TrendCategory:Date.Month"   -t Column \
  -a "TrendValue:Sales.Revenue"   -t Measure
```

## Spec — see examples

The KPI spec layers headline text, variance text, and a sparkline. Full working spec:

- `../examples/visual/kpi-card.json` — full PBIR visual block
- `../examples/spec/vega-lite/kpi-card.json` — spec-only

## Core layers

1. Headline value (large text) — `mark: text`
2. Variance pill (small text + background) — `mark: rect` + `mark: text`
3. Sparkline (line + dot) — `mark: line` + `mark: point`
4. Target reference line — `mark: rule`

Each layer reads from a different transform of `dataset` (filtered, aggregated, last-point).

## Don't reinvent

Start from `../examples/visual/kpi-card.json` and modify. Hand-rolling a Deneb KPI from scratch is a 4–6 hour exercise; modifying the example takes 30 minutes.
