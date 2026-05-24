# P3 — Sort-independent cumulative (the "Easy Pareto" trick)

The Pareto line itself: the **running sum of the share-of-total** ([P2](share-of-total.md)),
accumulated in descending-value order. This is the one primitive that makes the recipe
"easy" — it replaces a model `RANKX` column *and* a cumulative `CALCULATE` measure with a
single visual calculation.

## The naive version (the "before") — and why it breaks

```dax
Pareto = RUNNINGSUM ( [Percent of grand total] )
```

`RUNNINGSUM` accumulates **in the visual's current display order**. While the bars are
sorted by value descending, this is a correct Pareto curve. But sort the axis by anything
else — alphabetical, by a second column, by the user clicking a header — and the running
sum follows that order, producing a jagged line that no longer reads as "cumulative
contribution". The source keeps this as a hidden `Pareto` series purely as the contrast.

## The fix — pin the order with `ORDERBY`

```dax
Easy Pareto =
RUNNINGSUM ( [Percent of grand total], ORDERBY ( [<VALUE_MEASURE>], DESC ) )
```

The optional second argument of `RUNNINGSUM` is an **explicit accumulation order**.
`ORDERBY([<VALUE_MEASURE>], DESC)` says "always sum biggest-value-first", *independent of how
the visual is sorted*. Now the cumulative is a true Pareto curve no matter what the axis
sort is. That single argument is the whole recipe.

## Where it sits — `Y2` projection

```json
{
  "field": {
    "NativeVisualCalculation": {
      "Language": "dax",
      "Expression": "RUNNINGSUM([Percent of grand total], ORDERBY([<VALUE_MEASURE>], DESC))",
      "Name": "Easy Pareto"
    }
  },
  "queryRef": "select2",
  "nativeQueryRef": "Easy Pareto",
  "format": "0%;-0%;0%"
}
```

- On `Y2` (the secondary / line axis), so it draws as a line over the columns.
- `format: "0%..."` renders it as a percentage (the share is a 0–1 fraction).
- `queryRef: "select2"` — the conditional bar fill and label colors in [P4](threshold-split-emphasis.md)
  reference `select2`. Keep the alias.
- The hidden naive `Pareto` (if kept) sits just before it as `select1`.

## Rules

- **`ORDERBY` is mandatory.** Without it the curve is silently wrong after any re-sort — the
  bug looks like "the line zig-zags" and is easy to miss in the default sorted view.
- `[Percent of grand total]` must be defined on the visual already (P2) — visual calcs can
  only reference calcs/measures present on the same visual.
- Sort by the **same measure** in `ORDERBY` as the visual's `sortDefinition` (P1) so the
  line and bars agree in the default view.

## Generalises to

- Cumulative *value* instead of % — `RUNNINGSUM([<VALUE_MEASURE>], ORDERBY([<VALUE_MEASURE>], DESC))` on a value-scaled secondary axis.
- "How many categories make 80%?" — pair with a count visual calc, or use the [model-measure variant](../variants/model-measure-pareto.md) when you need that number outside the chart.

## Next

[P4 — threshold split + emphasis](threshold-split-emphasis.md) colors the line and bars at the 80% mark.
