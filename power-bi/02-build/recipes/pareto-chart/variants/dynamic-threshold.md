# Variant — Dynamic threshold

Let the user **drag the Pareto cutoff** (70% / 80% / 90% …) instead of hard-coding `0.8`.
The line re-splits and the bars re-color live. This is where the Pareto recipe *composes
with* [disconnected-selection-emphasis](../../disconnected-selection-emphasis/context.md):
a disconnected slicer harvested into one `[Selected Threshold]` measure that replaces every
`0.8` literal.

## Deltas from the base recipe

| Piece | Change |
|---|---|
| Model (P1 of the other recipe) | add a tiny disconnected table of threshold values — `GENERATESERIES(0.5, 0.95, 0.05)` — and a harvester measure. |
| P4 split | `GreenLine`/`RedLine` compare to `[Selected Threshold]` instead of `<THRESHOLD>`. |
| P4 bar fill | the conditional fill compares `select2` to `[Selected Threshold]` — but a JSON `Literal` can't hold a measure, so move the test *into a visual calc* (below). |
| P5 | unchanged. |

## The threshold input

```tmdl
table 'Threshold Slicer'
	column Threshold
		formatString: 0%
		summarizeBy: none
		sourceColumn: [Threshold]
	partition 'Threshold Slicer' = calculated
		mode: import
		source = GENERATESERIES ( 0.5, 0.95, 0.05 )
```

```dax
Selected Threshold = SELECTEDVALUE ( 'Threshold Slicer'[Threshold], 0.8 )
```

No relationship — selection is a pure input (the disconnected-selection idea). Default `0.8`
when nothing is picked.

## Re-express the split against the measure

Visual calcs *can* reference a model measure that's on the visual, so add `Selected Threshold`
to the visual (Tooltips well) and compare to it:

```dax
GreenLine = IF ( [Easy Pareto] <= [Selected Threshold], [Easy Pareto] )
RedLine   = IF ( [Easy Pareto] >  [Selected Threshold], [Easy Pareto] )
```

For the **bar fill**, the JSON `Conditional` can't embed a measure literal, so gate the color
in a visual calc and bind *that*:

```dax
Bar Color =
IF ( [Easy Pareto] <= [Selected Threshold], "<VITAL_COLOR>", "<TRIVIAL_COLOR>" )
```

Bind `Bar Color` to `dataPoint.fill` (with the `dataViewWildcard` selector — see
[P4](../primitives/threshold-split-emphasis.md)). This mirrors the disconnected recipe's
[category-spotlight](../../disconnected-selection-emphasis/variants/category-spotlight.md)
color-measure approach.

## Requirement — the measure must be ON the visual

`[Selected Threshold]` has to be present in the visual for the visual calcs to see it — add
it to the **Tooltips** projection (it doubles as a readout of the active cutoff). Omit it and
you get *"Column 'Selected Threshold' cannot be found"* at the visual-calc line. Same rule as
the disconnected recipe's
[conditional-series primitive](../../disconnected-selection-emphasis/primitives/conditional-series-visual-calc.md).

## Use when

- Reviewers argue about where the cutoff is — let them set it.
- Teaching the 80/20 idea interactively.

## Note

This is the most general form: the cutoff is data-driven, so the same chart serves 70/80/90
analyses. Selection still doesn't filter — it only moves the color boundary.
