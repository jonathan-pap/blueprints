# P1 — Sorted combo base

The foundation: a **line + stacked column combo** (`lineStackedColumnComboChart`) with the
category on the axis and the value measure as columns, **sorted descending by the value**.
The columns are the magnitude; the secondary (line) axis will later carry the cumulative %.
The descending sort is what turns an ordinary bar chart into a Pareto — biggest
contributors first, so the cumulative line bends early.

## Why this visual type

`lineStackedColumnComboChart` gives you two value wells (`Y` for columns, `Y2` for the
line) sharing one category axis, each on its own value axis. Pareto needs exactly that: a
magnitude axis (currency/count) and a 0–100% axis for the cumulative. A plain column or
line chart can't show both scales.

## The query skeleton

```json
"query": {
  "queryState": {
    "Category": {
      "projections": [
        { "field": { "Column": { "Expression": { "SourceRef": { "Entity": "<CATEGORY_TABLE>" } }, "Property": "<CATEGORY_COLUMN>" } },
          "queryRef": "<CATEGORY_TABLE>.<CATEGORY_COLUMN>", "nativeQueryRef": "<CATEGORY_COLUMN>", "active": true }
      ]
    },
    "Y":  { "projections": [ /* <VALUE_MEASURE> + the share visual calc (P2) */ ] },
    "Y2": { "projections": [ /* the cumulative + split visual calcs (P3, P4) */ ] }
  },
  "sortDefinition": {
    "sort": [
      { "field": { "Measure": { "Expression": { "SourceRef": { "Entity": "<MEASURE_TABLE>" } }, "Property": "<VALUE_MEASURE>" } },
        "direction": "Descending" }
    ],
    "isDefaultSort": true
  }
}
```

## The bars — `Y` projection

```json
{ "field": { "Measure": { "Expression": { "SourceRef": { "Entity": "<MEASURE_TABLE>" } }, "Property": "<VALUE_MEASURE>" } },
  "queryRef": "<MEASURE_TABLE>.<VALUE_MEASURE>", "nativeQueryRef": "<VALUE_MEASURE>" }
```

## Rules

- **Sort descending by `<VALUE_MEASURE>`** with `isDefaultSort: true`. This is the visible
  Pareto order. (The cumulative in [P3](sort-independent-cumulative.md) is robust to *any*
  sort, but the bars only read as a Pareto when they descend.)
- One category column on `Category`, one base measure on `Y`. Everything else on the visual
  is a visual calculation derived from these two.
- Keep the legend off — the green/red split is explained by color, not a legend.

## Generalises to

- Any "ranked contribution" chart. Swap `<VALUE_MEASURE>` for a count → the [count variant](../variants/count-pareto.md); the base stays identical.

## Next

[P2 — share of total](share-of-total.md) adds the first visual calculation.
