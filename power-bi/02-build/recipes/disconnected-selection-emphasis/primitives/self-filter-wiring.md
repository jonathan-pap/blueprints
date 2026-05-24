# P5 — Self-filter wiring

Because the [selection table is disconnected](disconnected-selection-table.md), it cannot
propagate filters through relationships. Two pieces of wiring make the recipe behave:

1. **The slicer carries its own visual-level filter** — its default range/selection.
2. **The chart carries its own axis + value filters** — to scope what it plots, independent of the (non-filtering) selection.

This is the deliberate split: **selection drives emphasis; these filters drive data scope.**

## Slicer self-filter (`filterConfig` on the slicer visual)

```json
"filterConfig": {
  "filters": [
    {
      "name": "<FILTER_NAME_SLICER>",
      "field": { "Column": {
        "Expression": { "SourceRef": { "Entity": "<SELECTION_TABLE_NAME>" } },
        "Property": "<SOURCE_COLUMN>" } },
      "type": "Categorical"
    }
  ]
}
```

The **default range** itself is set in the slicer's `objects.data` (date slicer) — `startDate` / `endDate` / `mode: 'Between'`:

```json
"data": [ { "properties": {
  "startDate": { "expr": { "Literal": { "Value": "<DEFAULT_START>" } } },
  "endDate":   { "expr": { "Literal": { "Value": "<DEFAULT_END>" } } },
  "mode":      { "expr": { "Literal": { "Value": "'Between'" } } }
} } ]
```

And the slicer's `objects.general.filter` holds the matching `And(>= start, <= end)` condition (ComparisonKind 2 = `>=`, 3 = `<=`). See the [slicer template](../templates/slicer.visual.json).

## Chart self-filters (`filterConfig` on the chart visual)

```json
"filterConfig": {
  "filters": [
    { "name": "<FILTER_NAME_VALUE>",
      "field": { "Measure": { "Expression": { "SourceRef": { "Entity": "<MEASURE_TABLE>" } },
                              "Property": "<VALUE_MEASURE>" } },
      "type": "Advanced" },
    { "name": "<FILTER_NAME_AXIS>",
      "field": { "Column": { "Expression": { "SourceRef": { "Entity": "<SOURCE_TABLE>" } },
                             "Property": "<AXIS_COLUMN>" } },
      "type": "Categorical" }
  ]
}
```

- The **Advanced** measure filter (e.g. `<VALUE_MEASURE>` is not blank) trims empty axis points.
- The **Categorical** axis filter scopes the plotted range.

## Comparison kinds & literals

| ComparisonKind | Operator |
|---|---|
| 2 | `>=` |
| 3 | `<=` |
| 0 | `=` · 1 `<>` · 4 `>` · 5 `<` |

Date literals are `datetime'YYYY-MM-DDThh:mm:ss'`. Note the original skill offsets the *display* default (`01:00:00`) from the *filter* bound (`00:00:00`, and the end bound is the **day after** the end date) so the boundary day is fully included.

## Rules

- Don't add a relationship to "fix" filtering — that breaks P1. Scope with these filters instead.
- Fresh hex IDs for every `filter.name` (20-char) — see [tokens.md](../tokens.md).

## Back to

[workflow.md](../workflow.md) assembles all five primitives in order.
