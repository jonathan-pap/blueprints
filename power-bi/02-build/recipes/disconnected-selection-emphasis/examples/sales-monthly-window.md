# Worked example — Sales monthly window highlight

The original skill, applied end-to-end: a `Sales` line by `EOmonth`, with a date-range
slicer that shades the selected window and labels only the in-window points.

## Token values

| Token | Value |
|---|---|
| `<SELECTION_TABLE_NAME>` | `dimDate Slicer` |
| `<SOURCE_TABLE>` | `dimDate` |
| `<SOURCE_COLUMN>` | `Date` |
| `<AXIS_COLUMN>` | `EOmonth` |
| `<MEASURE_TABLE>` | `_Measures` |
| `<VALUE_MEASURE>` | `Sales` |
| `<WINDOW_START_MEASURE>` | `Window Start Date` |
| `<WINDOW_END_MEASURE>` | `Window End Date` |
| `<WINDOW_CALC_NAME>` | `Data Labels Window` |
| `<CHART_TITLE>` | `Sales` |
| `<DEFAULT_START>` | `datetime'2025-08-30T01:00:00'` |
| `<DEFAULT_END>` | `datetime'2026-06-27T01:00:00'` |
| `<FILTER_START>` | `datetime'2025-08-30T00:00:00'` |
| `<FILTER_END>` | `datetime'2026-06-28T00:00:00'` |
| `<SELECTION_TABLE_LINEAGE_TAG>` | `4043821c-b0f7-4c37-8bc5-b40d2aadee9a` |
| `<SELECTION_COLUMN_LINEAGE_TAG>` | `0a04fbc5-36e8-4e1b-8e16-0174dfd1bdbe` |
| `<SELECTION_TABLE_PBI_ID>` | `1ce96267a7de4a62afe0bcb32964a8f9` |
| `<WINDOW_START_LINEAGE_TAG>` | `78e9a5f8-ead6-4eac-9465-dbf4a20b1323` |
| `<WINDOW_END_LINEAGE_TAG>` | `15a27af7-0669-4a4d-95ed-97e2d18a50ab` |
| `<VISUAL_NAME_SLICER>` | `b3734404e96bdca0e3d2` |
| `<VISUAL_NAME_CHART>` | `c1c97d02ce9912d08174` |
| `<FILTER_NAME_SLICER>` | `98ddb8015097c5696056` |
| `<FILTER_NAME_VALUE>` | `1800a24cb77220311b60` |
| `<FILTER_NAME_AXIS>` | `e70a12013c10005427d5` |
| `<PAGE_ID>` | `2904eb2c583866b57ec8` |
| slicer pos | x 1277.78 · y 240 · z 1 · h 87.78 · w 261.11 · tab 1 |
| chart pos | x 878.89 · y 218.89 · z 0 · h 430 · w 712.22 · tab 0 |

## Step 1 — `SemanticModel/definition/tables/dimDate Slicer.tmdl`

```tmdl
table 'dimDate Slicer'
	lineageTag: 4043821c-b0f7-4c37-8bc5-b40d2aadee9a

	column Date
		formatString: Short Date
		lineageTag: 0a04fbc5-36e8-4e1b-8e16-0174dfd1bdbe
		summarizeBy: none
		isNameInferred
		sourceColumn: dimDate[Date]

		annotation SummarizationSetBy = Automatic

	partition 'dimDate Slicer' = calculated
		mode: import
		source = VALUES( dimDate[Date] )

	annotation PBI_Id = 1ce96267a7de4a62afe0bcb32964a8f9
```

## Step 2 — append to `_Measures.tmdl` (before its `partition` line)

```tmdl
	measure 'Window Start Date' = MIN('dimDate Slicer'[Date])
		formatString: General Date
		lineageTag: 78e9a5f8-ead6-4eac-9465-dbf4a20b1323

	measure 'Window End Date' = MAX( 'dimDate Slicer'[Date])
		formatString: General Date
		lineageTag: 15a27af7-0669-4a4d-95ed-97e2d18a50ab
```

## Step 3 — append to `model.tmdl`

```tmdl
ref table 'dimDate Slicer'
```

## Steps 4–5 — the two visuals

Copy [templates/slicer.visual.json](../templates/slicer.visual.json) and
[templates/chart-with-band.visual.json](../templates/chart-with-band.visual.json) into
`Report/definition/pages/2904eb2c583866b57ec8/visuals/<name>/visual.json` and apply the
token values above. The chart's gated series resolves to:

```dax
Data Labels Window =
IF (
    [EOmonth] >= [Window Start Date]
        && [EOmonth] <= [Window End Date],
    [Sales]
)
```

## Result

- One disconnected `dimDate Slicer` table, no relationships.
- A date "Between" slicer; dragging it moves the shaded band (ref lines at Min/Max of the selection) and the visible data labels together.
- Tooltip shows `Window Start Date` / `Window End Date`.
