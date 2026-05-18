# DAX016 — Experiment with relationship overrides via TREATAS and CROSSFILTER

Relationship direction and filter propagation directly affect SE query plans. Sometimes bidirectional is faster; sometimes explicit filter propagation wins. Use TREATAS and CROSSFILTER to experiment without model changes.

## Example — replace bidirectional bridge with explicit filter

```dax
CALCULATE(
    SUM('Sales'[Amount]),
    CROSSFILTER('Customer'[CustomerKey], 'SportBridge'[CustomerKey], NONE),
    TREATAS(VALUES('SportBridge'[CustomerKey]), 'Customer'[CustomerKey])
)
```

## Signal

Bidirectional or M2M relationship causing unexpected SE join expansion. Existing `TREATAS` / `CROSSFILTER` in a measure (means someone already started experimenting — likely worth optimizing further).

## Escalation

If overrides consistently help across many measures, the actual fix is a model change. See `../model-tuning/mdl001-many-to-many.md`.
