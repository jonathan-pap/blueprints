# P2 — Boundary / harvester measures

Measures that read the slicer selection back off the [disconnected table](disconnected-selection-table.md).
"Harvester" = it harvests what the user picked. These are the bridge between the
unrelated slicer and every visual element that reacts to it.

## Range selection (two boundaries)

```tmdl
	measure '<WINDOW_START_MEASURE>' = MIN( '<SELECTION_TABLE_NAME>'[<SOURCE_COLUMN>] )
		formatString: General Date
		lineageTag: <WINDOW_START_LINEAGE_TAG>

	measure '<WINDOW_END_MEASURE>' = MAX( '<SELECTION_TABLE_NAME>'[<SOURCE_COLUMN>] )
		formatString: General Date
		lineageTag: <WINDOW_END_LINEAGE_TAG>
```

`MIN`/`MAX` collapse the selected set to its edges → the band. Works for dates and numbers alike (drop the `formatString` for numbers, or use `#,0`).

## Single selection (one value)

```tmdl
	measure '<SELECTED_VALUE_MEASURE>' = SELECTEDVALUE( '<SELECTION_TABLE_NAME>'[<SOURCE_COLUMN>] )
		lineageTag: <SELECTED_VALUE_LINEAGE_TAG>
```

Use for comparison-period (one quarter) or single-threshold variants.

## Why these work without a relationship

The slicer applies a filter to the disconnected table only. `MIN`/`MAX`/`SELECTEDVALUE`
evaluate in that filter context and return the picked edge(s). Nothing propagates to
the fact tables — so the harvested numbers describe the *selection*, not a filter on data.

## Rules

- Name them for the role, not the type (`Window Start Date`, `Threshold Low`).
- These are safe to show in tooltips so users can read the active selection.
- If the slicer is cleared, `MIN`/`MAX` return the full domain edges — decide whether that's the desired "no selection" behaviour or guard with `ISFILTERED`.

## Next

[P3 — reference-band shading](reference-band-shading.md) draws the band at these measures; [P4 — conditional series](conditional-series-visual-calc.md) gates a series by them.
