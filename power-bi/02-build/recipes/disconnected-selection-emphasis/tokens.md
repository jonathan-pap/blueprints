# Tokens

Substitute every `<TOKEN>` across the [templates](templates/) before writing files.
Grouped by what they identify. Generic names (source-agnostic) so the recipe works for
date, numeric, or category sources.

## Model — names

| Token | Description | Example |
|---|---|---|
| `<SELECTION_TABLE_NAME>` | New disconnected table | `dimDate Slicer` |
| `<SOURCE_TABLE>` | Existing table the selection mirrors | `dimDate` |
| `<SOURCE_COLUMN>` | Column to select on (date/number/category) | `Date` |
| `<MEASURE_TABLE>` | Table that holds measures | `_Measures` |
| `<VALUE_MEASURE>` | Existing measure to plot | `Sales` |
| `<AXIS_COLUMN>` | Chart category/X axis column | `EOmonth` |
| `<WINDOW_START_MEASURE>` | Harvester: MIN of selection | `Window Start Date` |
| `<WINDOW_END_MEASURE>` | Harvester: MAX of selection | `Window End Date` |
| `<SELECTED_VALUE_MEASURE>` | Harvester: SELECTEDVALUE (single-pick variants) | `Selected Quarter` |
| `<WINDOW_CALC_NAME>` | Visual-calculation series name | `Data Labels Window` |
| `<CHART_TITLE>` | Chart title text | `Sales` |

## IDs — generate fresh per build

| Token | Format | How |
|---|---|---|
| `<SELECTION_TABLE_LINEAGE_TAG>` | UUID | `uuidgen` |
| `<SELECTION_COLUMN_LINEAGE_TAG>` | UUID | `uuidgen` |
| `<WINDOW_START_LINEAGE_TAG>` / `<WINDOW_END_LINEAGE_TAG>` | UUID | `uuidgen` |
| `<SELECTION_TABLE_PBI_ID>` | 32-char hex | `python -c "import uuid;print(uuid.uuid4().hex)"` |
| `<VISUAL_NAME_SLICER>` / `<VISUAL_NAME_CHART>` | 20-char hex | `python -c "import uuid;print(uuid.uuid4().hex[:20])"` |
| `<FILTER_NAME_SLICER>` / `<FILTER_NAME_VALUE>` / `<FILTER_NAME_AXIS>` | 20-char hex | as above |

Reuse the same `<PAGE_ID>` as the page you're adding the visuals to (an existing 20-hex page folder name).

## Selection literals (date variant)

| Token | Description | Example |
|---|---|---|
| `<DEFAULT_START>` | Slicer default start (display) | `datetime'2025-08-30T01:00:00'` |
| `<DEFAULT_END>` | Slicer default end (display) | `datetime'2026-06-27T01:00:00'` |
| `<FILTER_START>` | Filter lower bound (midnight, start day) | `datetime'2025-08-30T00:00:00'` |
| `<FILTER_END>` | Filter upper bound (midnight, **day after** end) | `datetime'2026-06-28T00:00:00'` |

For **numeric** variants these become plain number literals and the slicer `mode` changes — see [numeric-threshold-band](variants/numeric-threshold-band.md).

## Layout

| Token | Description |
|---|---|
| `<SLICER_X/Y/Z/HEIGHT/WIDTH/TAB_ORDER>` | Slicer position + size |
| `<CHART_X/Y/Z/HEIGHT/WIDTH/TAB_ORDER>` | Chart position + size |

## Bulk substitution

```bash
# from the project root, after copying a template to its destination
sed -i \
  -e "s/<SELECTION_TABLE_NAME>/dimDate Slicer/g" \
  -e "s/<SOURCE_TABLE>/dimDate/g" \
  -e "s/<SOURCE_COLUMN>/Date/g" \
  path/to/written/file
```
