# Variant — vs Prior Year

The same chart, but the benchmark is **last year** instead of a target. "Did we grow on this
month last year, and by how much?" Mechanically it's a one-measure swap — `<TARGET_MEASURE>`
becomes a prior-year measure — everything else (overlay, connectors, label, narrative) is
identical.

## Deltas from the base recipe

| Piece | Change |
|---|---|
| `<TARGET_MEASURE>` | replace with a time-intelligence prior-year measure |
| `Delta` | now reads "vs PY"; relabel the connector legend / subtitle wording |
| P2 / P3 / P4 / P5 | unchanged |

## The prior-year measure

```dax
<ACTUAL_MEASURE> PY =
CALCULATE ( [<ACTUAL_MEASURE>], DATEADD ( <DATE_TABLE>[Date], -1, YEAR ) )
```

Then point every `[<TARGET_MEASURE>]` reference in [variance-measures.tmdl](../templates/variance-measures.tmdl)
at `[<ACTUAL_MEASURE> PY]`:

```dax
Delta     = [<ACTUAL_MEASURE>] - [<ACTUAL_MEASURE> PY]
% Delta   = DIVIDE ( [Delta], [<ACTUAL_MEASURE> PY] )   -- "▲0%;▼0%;0%"
MAX VALUE = IF ( [<ACTUAL_MEASURE>] > [<ACTUAL_MEASURE> PY], [<ACTUAL_MEASURE>], [<ACTUAL_MEASURE> PY] )
```

`GREEN MAX` / `RED MAX` / `Delta Color` are unchanged — they read `Delta` and `MAX VALUE`.

## Wording

- Outline ("ghost") bar = **PY**; filled bar = **this year**.
- Subtitle: *"…we grew on last year in N months, strongest in March, longest growth streak 4."*
  (relabel `TAKEAWAY` and `Number Successful Months` → "growth months").

## Use when

- Trend reviews framed as growth vs the comparable prior period.
- No formal target exists, but year-over-year is the de-facto benchmark.

## Note

Works with any comparison period — prior month (`DATEADD(...,-1,MONTH)`), same period last
year, a frozen budget snapshot. The recipe doesn't care what the "ghost" bar represents, only
that there are two series to bracket.
