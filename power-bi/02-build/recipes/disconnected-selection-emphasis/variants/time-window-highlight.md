# Variant — Time-window highlight (the original)

Highlight a user-selected **date range** on a line chart: shaded band between two dates,
data labels only inside the window. This is the recipe applied with a date source — no deltas.

## Spec

| Primitive | Choice |
|---|---|
| P1 source | `VALUES( <SOURCE_TABLE>[<DATE_COLUMN>] )` |
| P2 harvest | `MIN` / `MAX` → `Window Start Date` / `Window End Date` |
| P3 band | `xAxisReferenceLine`, Function 3 (start) + 4 (end), shade `'before'` |
| P4 series | visual calc: value when `[<AXIS_COLUMN>] >= Start && <= End` |
| P5 slicer | date slicer, `mode: 'Between'`, default `startDate`/`endDate` |

## Notes specific to dates

- Axis column is often a period column (`EOmonth`) distinct from the slicer's day-grain `Date` — that's fine, the visual calc compares the axis column to the harvested dates.
- Mind the midnight offsets: filter lower bound at `00:00:00` of the start day, upper bound at `00:00:00` of the **day after** the end day, so both boundary days are included. Display defaults can sit at `01:00:00`.
- `formatString: General Date` on the harvester measures so tooltips read cleanly.

## Build

Follow [workflow.md](../workflow.md) verbatim with the date tokens from [tokens.md](../tokens.md).
Worked end-to-end: [examples/sales-monthly-window.md](../examples/sales-monthly-window.md).
