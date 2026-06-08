# Add a table

Flat row list. For hierarchies, use `matrix.md`.

## Create

```bash
pbir add visual tableEx "<project>.Report/Overview.Page" --title "Order Details" \
  --x 24 --y 540 --width 1232 --height 196
```

## Bind fields

```bash
pbir visuals bind "<...>/Order Details.Visual" \
  -a "Values:Customers.Key Account Name" -t Column \
  -a "Values:Products.Product Name"      -t Column \
  -a "Values:Sales.Revenue"              -t Measure \
  -a "Values:Sales.Orders"               -t Measure
```

## Sort

Usually descending by the most important measure (often variance, not alphabetical):

```bash
pbir visuals sort "<...>/Order Details.Visual" -f "Sales.Revenue" -d Descending
```

## Format philosophy

Subtract, don't add. Remove gridlines, banding, default borders — let whitespace separate rows. Apply data bars to the primary measure and color scales to variance columns only.

## Pitfall — never write `active` on `tableEx` projections

Hand-written `tableEx` visual.json renders an empty body (chrome + fields panel bind, no rows) whenever ANY projection in `query.queryState.Values.projections[*]` has the `active` field set — symmetrically or not. The only working form omits `active` entirely on every projection:

```json
"projections": [
  { "field": { "Column":  {...} }, "queryRef": "...", "nativeQueryRef": "..." },
  { "field": { "Measure": {...} }, "queryRef": "...", "nativeQueryRef": "..." },
  { "field": { "Measure": {...} }, "queryRef": "...", "nativeQueryRef": "..." }
]
```

Confirmed against a 5-variant stress test on grand-exchange 2026-06-04:

| Variant | `active` flags | Renders? |
| --- | --- | --- |
| A · Minimal (2 cols) | none | rows |
| B · Explicit consistent (dim:true + measures:false) | present | empty body |
| C · Wide 5-col | none | rows |
| D · Sorted via `sortDefinition` | none | rows |
| E · Different dim | none | rows |

Chart visualTypes (`barChart`, `lineChart`, `donutChart`, `card`, `lineStackedColumnComboChart`) all tolerate `active: true` on Category. `tableEx` specifically does not — strip it before pasting any snippet from a working chart.

Desktop's auto-fix that adds `active: false` to each measure when it reformats a broken table does NOT actually fix the rendering — it just makes the flags symmetric while leaving the table broken. Always verify the rendered result, not just the post-fix file.

## Pitfall — heavy iterative measures in one tableEx blow up the query plan

Putting 2+ measures with N×N iteration patterns into the same `tableEx` at row granularity (item / customer / SKU) can blow up the query plan and render an empty body even when each measure runs fine alone. The chrome shows, projections bind, no rows appear — and no error toast.

Patterns to flag before binding:

- `MEDIANX(VALUES(...), ...)` — O(N) per row × N rows = O(N²)
- Per-day price/correlation/drawdown walks (`52W High`, `Max Drawdown 90D %`, rolling correlation)
- Measure-calls-measure with FE-side iteration (`Blue Ocean Score` invoking `Substitute Density` internally; both listed in the same table double-evaluates the heavier one)
- Nested `CALCULATE` + `ALLEXCEPT` rebuilds the filter context per row

Triage:

1. **Keep cheap aggregates in the table** — `Total Trade Value`, `Trade Quantity`, `Avg Close Price`, `VWAP`, basic flow ratios.
2. **Move heavy measures to KPI cards** on the same page — cards evaluate once at the filtered context, not per row.
3. **Promote to a calculated column** on the dim if a heavy measure is genuinely needed per row — runs at refresh time, not query time.

Confirmed against grand-exchange Blue Ocean table (4 measures, empty body) and Risk table (`Max Drawdown 90D %` + `Optionality Asymmetry`, empty body) on 2026-06-04.

## Templates

- `../examples/visuals/default/tableEx.json`
- `../examples/visuals/formatted/tableEx-gradient.json` — color-scale gradient on a measure column

## After

`../validate/validate.md`. Consider `../format/conditional-fmt-data-bar.md` for the magnitude column.
