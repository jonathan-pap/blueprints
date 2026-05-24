# P4 — Threshold split + emphasis

The "80/20" payload: split the cumulative line into a **green segment up to the threshold**
and a **red segment beyond it**, and color the **bars** to match. The eye lands on the cutoff
— the vital few (green) vs. the trivial many (red) — without anyone reading a number.

Two independent emphases, both keyed off `[Easy Pareto]` (P3):

## 1. Split the line into two series

```dax
GreenLine = IF ( [Easy Pareto] - [Percent of grand total] < <THRESHOLD>, [Easy Pareto] )  -- vital few (+ crossing bar)
RedLine   = IF ( [Easy Pareto] > <THRESHOLD>, [Easy Pareto] )                              -- trivial many
```

`BLANK` outside each segment → that part of the line isn't drawn. Two `Y2` projections
(`queryRef` `select3`, `select4`), styled teal `<VITAL_COLOR>` and red `<TRIVIAL_COLOR>` in
`objects.lineStyles` / `objects.dataPoint` (selected by `metadata: select3` / `select4`).
The shown `Easy Pareto` line (`select2`) carries the markers + data labels; the two
split series carry the colored strokes.

**Continuous line, no gap (the load-bearing detail).** A naive split —
`GreenLine = IF([Easy Pareto] <= <THRESHOLD>, …)` and `RedLine = IF([Easy Pareto] > <THRESHOLD>, …)` —
leaves green and red with **no shared point** (the last green bar is ≤80%, the first red bar
is >80%), so the two strokes can't join: you get a one-segment **gap** at the cutoff. The fix
is to extend green to the **first bar that crosses** the threshold so it overlaps red by one
point: `[Easy Pareto] - [Percent of grand total]` is the cumulative *before* this bar — if
that was still under the threshold, this bar is the crossing point and stays green. Now the
line is continuous and simply flips color. (Comparing to `>= <THRESHOLD>` does **not** fix
it — real cumulative values never land exactly on the cutoff.)

> Alternative: keep the naive `<=` split but draw red **markers-only** (`strokeShow: false`
> on `select4`) — then there's no red stroke to disconnect (green line → red dots). The
> original source export does this; option A above is the continuous-line upgrade.

```json
{ "field": { "NativeVisualCalculation": { "Language": "dax",
    "Expression": "IF([Easy Pareto] - [Percent of grand total] < <THRESHOLD>, [Easy Pareto], BLANK())", "Name": "GreenLine" } },
  "queryRef": "select3", "nativeQueryRef": "GreenLine" },
{ "field": { "NativeVisualCalculation": { "Language": "dax",
    "Expression": "IF([Easy Pareto]><THRESHOLD>,[Easy Pareto],BLANK())", "Name": "RedLine" } },
  "queryRef": "select4", "nativeQueryRef": "RedLine" }
```

## 2. Color the bars by the same cutoff

A conditional `dataPoint.fill` that reads `select2` (`Easy Pareto`) per bar: red when the
bar's cumulative is past the threshold, teal when it's within it.

```json
"dataPoint": [
  {
    "properties": { "fill": { "solid": { "color": { "expr": { "Conditional": { "Cases": [
      { "Condition": { "Comparison": { "ComparisonKind": 1,
          "Left": { "SelectRef": { "ExpressionName": "select2" } },
          "Right": { "Literal": { "Value": "<THRESHOLD>D" } } } },
        "Value": { "Literal": { "Value": "'<TRIVIAL_COLOR>'" } } },
      { "Condition": { "And": {
          "Left":  { "Comparison": { "ComparisonKind": 2, "Left": { "SelectRef": { "ExpressionName": "select2" } }, "Right": { "Literal": { "Value": "0D" } } } },
          "Right": { "Comparison": { "ComparisonKind": 4, "Left": { "SelectRef": { "ExpressionName": "select2" } }, "Right": { "Literal": { "Value": "<THRESHOLD>D" } } } } } },
        "Value": { "Literal": { "Value": "'<VITAL_COLOR>'" } } }
    ] } } } } } },
    "selector": { "data": [ { "dataViewWildcard": { "matchingOption": 1 } } ] }
  }
]
```

`ComparisonKind`: `1` = greater-than, `2` = greater-or-equal, `4` = less-or-equal. So case 1
= "cumulative > 0.8 → red"; case 2 = "0 ≤ cumulative ≤ 0.8 → teal".

**Critical — the per-point selector.** A `SelectRef`/measure-driven `dataPoint.fill` must
carry `"selector": { "data": [ { "dataViewWildcard": { "matchingOption": 1 } } ] }` or it
evaluates once for the whole series — every bar gets the same color and it looks like nothing
conditionally formats. (Same gotcha as the disconnected recipe's
[category spotlight](../../disconnected-selection-emphasis/variants/category-spotlight.md).)

## Optional — label tints

The data labels on the `Easy Pareto` line can be tinted to match (`<VITAL_LABEL_COLOR>` /
`<TRIVIAL_LABEL_COLOR>`) with the same `select2`-vs-threshold conditional under
`objects.labels` (selector `metadata: select2` + the `dataViewWildcard`). Cosmetic; the
template includes it.

## Rules

- All four pieces (GreenLine, RedLine, bar fill, label tint) compare against the **same
  threshold** and the **same series** (`select2` / `[Easy Pareto]`). Change the cutoff in one
  place → change it everywhere, or the line split and bar colors disagree. The
  [dynamic-threshold variant](../variants/dynamic-threshold.md) makes that a single measure.
- Rule-based color via the CLI: see `../../report/format/conditional-fmt-rule.md`. For a
  measure-driven version, `pbir visuals cf … --measure …` writes the `dataViewWildcard`
  selector for you.

## Generalises to

- More than two bands → the [ABC classification variant](../variants/abc-classification.md) (A/B/C).
- A draggable cutoff → the [dynamic-threshold variant](../variants/dynamic-threshold.md).

## Next

[P5 — dual-axis plumbing](dual-axis-plumbing.md) fixes the secondary axis to 0–100% and tidies labels.
