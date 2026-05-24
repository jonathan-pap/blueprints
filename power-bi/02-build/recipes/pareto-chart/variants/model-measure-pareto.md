# Variant — Model-measure Pareto (the "hard way")

The traditional approach, before visual calculations existed: a `RANKX` **calculated column**
and a cumulative **measure** in the model. More work and slower to author than the base
recipe — but the right choice when you need the cumulative **outside the one chart** (a card
"top N products = 80% of sales", a table column, another visual) or you're on a Power BI
version without visual calculations.

This variant exists mainly as a **contrast**: it shows exactly what the
[Easy Pareto trick](../primitives/sort-independent-cumulative.md) replaces.

## Deltas from the base recipe

| Piece | Change |
|---|---|
| Model | **add** a rank column + a cumulative measure (touches `model.tmdl` indirectly via the table file). |
| P2 / P3 visual calcs | **removed** — the cumulative is now a model measure. |
| P4 split | reads the model `[<CUM_MEASURE_NAME>]` instead of a visual calc; same green/red logic. |
| P1 / P5 | unchanged (still a sorted combo with a 0–1 secondary axis). |

## 1. Rank the categories (calculated column on `<CATEGORY_TABLE>`)

```dax
<RANK_COLUMN_NAME> =
RANKX ( ALL ( '<CATEGORY_TABLE>'[<CATEGORY_COLUMN>] ), CALCULATE ( [<VALUE_MEASURE>] ),, DESC, DENSE )
```

A physical column so it can sort the axis and feed other visuals.

## 2. Cumulative % (measure)

```dax
<CUM_MEASURE_NAME> =
VAR _cur   = [<VALUE_MEASURE>]
VAR _grand = CALCULATE ( [<VALUE_MEASURE>], ALLSELECTED ( '<CATEGORY_TABLE>'[<CATEGORY_COLUMN>] ) )
VAR _cum =
    CALCULATE (
        [<VALUE_MEASURE>],
        FILTER (
            ALLSELECTED ( '<CATEGORY_TABLE>'[<CATEGORY_COLUMN>] ),
            CALCULATE ( [<VALUE_MEASURE>] ) >= _cur
        )
    )
RETURN DIVIDE ( _cum, _grand )
```

The `FILTER … >= _cur` sums every category whose value is at least the current one — i.e. the
cumulative in descending-value order, the model equivalent of `RUNNINGSUM(…, ORDERBY(DESC))`.
`ALLSELECTED` keeps it responsive to slicers while ignoring the axis's own filter.

> Template: [templates/model-measures.tmdl](../templates/model-measures.tmdl).

## Drawing the line — green/red as model measures

The base recipe splits the line with visual calcs; here they're model measures that read
`[<CUM_MEASURE_NAME>]`. Use the **continuous (overlap-by-one)** form so the two strokes join
into one color-flipping line (see [P4](../primitives/threshold-split-emphasis.md) for *why*
the naive `<=` / `>` split leaves a gap):

```dax
Cumulative Green =                       -- vital few + the first bar that crosses
VAR _grand = CALCULATE ( [<VALUE_MEASURE>], ALLSELECTED ( '<CATEGORY_TABLE>'[<CATEGORY_COLUMN>] ) )
VAR _prev  = [<CUM_MEASURE_NAME>] - DIVIDE ( [<VALUE_MEASURE>], _grand )   -- cumulative before this bar
RETURN IF ( _prev < 0.8, [<CUM_MEASURE_NAME>] )

Cumulative Red = IF ( [<CUM_MEASURE_NAME>] > 0.8, [<CUM_MEASURE_NAME>] )   -- trivial many
```

Plot both on the secondary axis, color teal / red, and color the bars with a
`Pareto Bar Color = IF ( [<CUM_MEASURE_NAME>] <= 0.8, "#1E9790", "#ED4D55" )` measure bound to
`dataPoint.fill` (with the `dataViewWildcard` selector). Because these are model measures they
evaluate per axis category — no visual calc needed.

## As seen in the wild — the community pattern (and one trap)

The widely-shared Fabric community write-up [*Create Pareto Chart in Power BI*](https://community.fabric.microsoft.com/t5/Power-BI-Community-Blog/Create-Pareto-Chart-In-Power-BI/ba-p/4362753)
builds exactly this variant. Its cumulative is the same "sum everything ≥ the current value"
idea, written with `SUMX` / `SUMMARIZE` instead of `CALCULATE` / `FILTER`:

```dax
-- Cumulative sales
VAR A = SUM ( Orders[Sales] )
RETURN
    SUMX (
        FILTER (
            SUMMARIZE ( ALL ( Orders ), Orders[Product Sub-Category], "revenue", [Sales_] ),
            [revenue] >= A
        ),
        [revenue]
    )

-- Cumulative %
VAR A = [Cumulative sales]
VAR B = CALCULATE ( [Sales_], ALL ( Orders ) )
RETURN DIVIDE ( A, B )

-- 80% threshold (a constant measure, plotted as a third series)
line = 0.8
```

It pairs these with a *Line and clustered column chart* (cumulative % on the secondary axis,
the `line` measure as a flat reference) rather than our green/red split — cosmetic.

**The trap: `ALL` vs `ALLSELECTED`.** The article wraps everything in `ALL ( Orders )`, which
strips **every** filter — including outer slicers. Drop a Region slicer on that page and the
Pareto won't recompute for the chosen region; the cumulative still reflects all data. Our
measure above uses `ALLSELECTED ( '<CATEGORY_TABLE>'[<CATEGORY_COLUMN>] )` instead, so it
clears only the **axis category** (to see across bars) while *respecting* slicers and page
filters. That's the same slicer-interactivity you protected in the
[base recipe](../context.md) — keep `ALLSELECTED` unless you deliberately want a
slicer-proof grand total.

Second, smaller trap: `[revenue] >= A` counts **every** category whose value ties the current
one, double-adding at ties — see *Cost vs. the base recipe* below.

## 3. Bonus — the number you can't get from a visual calc

Because it's a real measure, you can answer "how many categories make up 80%?" anywhere:

```dax
# Categories to 80% =
COUNTROWS ( FILTER ( VALUES ( '<CATEGORY_TABLE>'[<CATEGORY_COLUMN>] ), [<CUM_MEASURE_NAME>] <= 0.8 ) ) + 1
```

Drop that in a card. The base visual-calc recipe can't feed a card — its cumulative only
exists inside the chart. **That's the deciding factor between the two approaches.**

## Cost vs. the base recipe

- A `RANKX` column materializes per row and grows the model; the cumulative measure is an
  `O(n²)`-ish self-join pattern that's slower on high-cardinality categories.
- Ties need handling (`DENSE` rank, or add a tiebreaker to the `>=` filter) — the visual-calc
  version sidesteps this.

## Use when

- You need the cumulative / "N to 80%" in **cards, tables, or other visuals**, not just the Pareto chart.
- The target Power BI version predates visual calculations.

Otherwise prefer the [base recipe](../context.md) — fewer moving parts, no model bloat.
