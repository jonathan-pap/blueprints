# Add a matrix

Use when 2+ categorical columns form a hierarchy (e.g., Region › Account › Product). For a flat list use `table.md`.

## Create

```bash
pbir add visual pivotTable "<project>.Report/Overview.Page" --title "Sales Breakdown" \
  --x 24 --y 540 --width 1232 --height 220
```

## Bind fields

```bash
pbir visuals bind "<...>/Sales Breakdown.Visual" \
  -a "Rows:Geography.Region"        -t Column \
  -a "Rows:Customers.Key Account Name" -t Column \
  -a "Columns:Date.Calendar Quarter"  -t Column \
  -a "Values:Sales.Revenue"           -t Measure \
  -a "Values:Sales.Revenue 1YP"       -t Measure
```

## Field roles

- `Rows` (Column, repeatable) — hierarchy levels, ordered
- `Columns` (Column, repeatable) — pivot dimension
- `Values` (Measure, repeatable) — cell values

## Expand defaults

Matrix collapses to top level by default. Expand one level for executive views or all for detail views.

## Templates

- `../examples/visuals/default/pivotTable.json`
- `../examples/visuals/formatted/pivotTable-bullet-kpi.json` — inline bullet + KPI per row
- `../examples/visuals/formatted/pivotTable-flash.json` — animation / highlight variant

## After

`../validate/validate.md`.
