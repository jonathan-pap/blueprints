# P2 — Share of total

The first visual calculation: each category's value as a **fraction of the visual's grand
total**. It's the per-bar building block the cumulative ([P3](sort-independent-cumulative.md))
sums up. Hidden — it never displays; it only feeds the running sum.

## The visual calc

```dax
Percent of grand total =
DIVIDE ( [<VALUE_MEASURE>], COLLAPSEALL ( [<VALUE_MEASURE>], ROWS ) )
```

`COLLAPSEALL([<VALUE_MEASURE>], ROWS)` evaluates the measure with **all category rows
collapsed** — i.e. the grand total across every bar in the visual. Dividing the current
bar's value by that total gives its share. `DIVIDE` guards against an empty visual (no
divide-by-zero).

## Where it sits — `Y` projection, hidden

```json
{
  "field": {
    "NativeVisualCalculation": {
      "Language": "dax",
      "Expression": "DIVIDE([<VALUE_MEASURE>], COLLAPSEALL([<VALUE_MEASURE>], ROWS))",
      "Name": "Percent of grand total"
    }
  },
  "queryRef": "select",
  "nativeQueryRef": "Percent of grand total",
  "hidden": true
}
```

It lives on `Y` (next to the base measure) and is `hidden: true` — there's no reason to draw
per-bar percentages; they'd clutter the magnitude axis. Its only consumer is P3.

## Rules

- **Use `COLLAPSEALL(..., ROWS)`, not a model `ALL`/`ALLSELECTED`.** The grand total must be
  the *visual's* total (respecting the visual's own filters and the current axis), which is
  exactly what `COLLAPSEALL` over the visual's row axis gives. A model-level total would
  ignore visual-scope filtering.
- Keep it `hidden: true` and give it `queryRef: "select"` — P3/P4 and the formatting refer
  back to these aliases (`select`, `select1`, …) in projection order. See [tokens](../tokens.md).
- The name `Percent of grand total` is referenced verbatim by P3 (`[Percent of grand total]`)
  — don't rename one without the other.

## Why a visual calc (not a model measure)

"Share of *what's on the chart*" depends on the visual's row set and filters. A model
measure computing % of total would need to know the visual's category and filter context,
which it can't see. Visual calculations evaluate after the visual aggregates, so the
denominator is naturally the visible total. See `../../report/calculations/visual-calculation.md`.

## Next

[P3 — sort-independent cumulative](sort-independent-cumulative.md) running-sums this share.
