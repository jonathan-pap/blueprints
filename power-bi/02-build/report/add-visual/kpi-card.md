# Add a KPI card

Use when the user wants a single value with a target and trend line. Prefer `kpi` over `card` whenever a target exists.

## Prereqs

- Canonical measure names (run `../bind/find-canonical-name.md`).
- Target measure exists in the model (e.g., `'Sales'[Revenue 1YP]`). If not, ask the user before building.

## Create

```bash
pbir add visual kpi "<project>.Report/Overview.Page" --title "Revenue" \
  -d "Indicator:Sales.Revenue" \
  -d "Goal:Sales.Revenue 1YP" \
  -d "TrendLine:Date.Calendar Month (ie Jan)" \
  --x 24 --y 120 --width 400 --height 160
```

## Field roles

- `Indicator` (Measure, required) — the headline value
- `Goal` (Measure) — the target / comparison
- `TrendLine` (Column) — typically a date column

## After

- Hide the auto subtitle: `pbir visuals subtitle "<...>/Revenue.Visual" --no-show`
- Set the goal label: in the visual.json, set `goals.goalText` to `"1YP"`, `"Budget"`, etc.
- Validate: `../validate/validate.md`

## Templates

- `../examples/visuals/default/kpi.json` — bare KPI with theme defaults
- `../examples/visuals/formatted/kpi.json` — formatted KPI
- `../examples/visuals/formatted/kpi-flash.json` — flash / animation variant

## Wrong field type?

See `../bind/column-vs-measure.md`.
