# Add a combo chart (line + column)

Two measures on different scales. Common pattern: bar for absolute (revenue), line for ratio (margin %).

## Create

```bash
pbir add visual lineStackedColumnComboChart "<project>.Report/Overview.Page" \
  --name "lineStkColCombo" \
  --title "Revenue & Margin" \
  --x 24 --y 300 --width 700 --height 400
```

Other variant: `lineClusteredColumnComboChart` (un-stacked columns).

**`--name` required** for both combo variants — the auto-generated `<title>-<type>-<hash>` name overflows the PBIR schema length limit otherwise. Without it you get: `Schema validation failed for 'visual': name '…' is too long`.

## Bind fields

```bash
pbir visuals bind "<...>/Revenue & Margin.Visual" \
  -a "Category:Date.Month"   -t Column \
  -a "Y:Sales.Revenue"       -t Measure \
  -a "Y2:Sales.Margin %"     -t Measure
```

## Field roles

- `Category` (Column) — x-axis (usually time)
- `Y` (Measure) — **column** values, primary y-axis
- `Y2` (Measure) — **line** values, secondary y-axis (auto-scaled separately)
- `Series` (Column, optional) — split columns by category
- `Tooltips` (Column or Measure, optional)

Confirm with `pbir visuals bind "<...>" --list-roles` if uncertain — the role names differ from `lineChart` / `clusteredColumnChart` despite the family resemblance.

## When to use

- Absolute amount + percentage on the same x-axis (revenue + margin %, units + utilization rate).
- Volume + price.
- Anything where two measures have very different scales but the same temporal context.

## Templates

- `../examples/visuals/default/comboChart.json`
- `../examples/visuals/formatted/comboChart.json`
- `../examples/visuals/formatted/comboChart-flash.json`

## After

`../validate/validate.md`.
