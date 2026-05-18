# QRY002 — Eliminate report measure filters (`__ValueFilterDM`)

> Tier 2 — explicit user approval required before applying.

When a visual filters on a measure value (e.g., "Revenue > 1M"), Power BI generates a `__ValueFilterDM` variable that evaluates the measure twice — once for the filter check, once for display. Roughly doubles execution time.

## Detection

`__ValueFilterDM` in the generated query.

## Fix

Move the threshold into the measure itself — return BLANK below the cutoff. SUMMARIZECOLUMNS auto-drops blank rows, achieving the same visual result in one pass:

```dax
MEASURE 'Sales'[Total Revenue Filtered] =
    VAR __Rev = [Total Revenue]
    RETURN IF(__Rev > 1000000, __Rev)
```

## Desktop action

The user:

1. Adds the new `Total Revenue Filtered` measure to the model.
2. Replaces the original measure reference on the visual with the filtered version.
3. Removes the original measure-value filter (`Revenue > 1M`) from the visual filter pane.

The agent provides the measure definition; the user wires it up via the UI.

## Trade-off

The measure is now report-specific. If many visuals need different thresholds, you'd end up with many filtered measures — at that point, the original measure-value filter approach may be the better trade despite the perf cost.
