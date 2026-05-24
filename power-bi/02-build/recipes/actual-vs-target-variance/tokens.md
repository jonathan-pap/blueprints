# Tokens

Substitute every `<TOKEN>` across the [templates](templates/) before writing files.

## Data binding (the ones you must change)

| Token | Description | Example |
|---|---|---|
| `<MEASURE_TABLE>` | Table that holds the measures | `Mesures` |
| `<ACTUAL_MEASURE>` | The actual / current value | `NET SALES` |
| `<TARGET_MEASURE>` | The benchmark (target / budget / forecast / PY) | `TARGET SALES` |
| `<AXIS_TABLE>` | Table of the category axis | `Dim_Date` |
| `<AXIS_COLUMN>` | Axis column (usually a month label) | `MoisCourt_2_en` |
| `<MONTH_KEY_COLUMN>` | Sortable period key for the streak/best-month DAX (P5 only) | `MoisAnnéeNo` (e.g. `"012024"`) |
| `<YEAR_COLUMN>` | Year column for the narrative sentence (P5 only) | `Année` |

## Internal measure names (fixed — rename only in lockstep)

These are referenced across measures and in the visual's bindings/selectors. Keep as shipped
unless you rename every reference together.

| Name | Role |
|---|---|
| `Delta` | actual − target |
| `% Delta` | `Delta / target`, arrow-formatted |
| `MAX VALUE` | `max(actual, target)` — the transparent overlay series |
| `GREEN MAX` / `RED MAX` | `MAX VALUE` gated by `Delta > 0` / `< 0` — the error-bar bounds |
| `Delta Color` | green/red (or grey) hex by variance sign — drives the label color |
| `TAKEAWAY` (P5) | the narrative subtitle sentence |

The visual's series selectors key off the **metadata** `<MEASURE_TABLE>.<ACTUAL_MEASURE>`,
`<MEASURE_TABLE>.<TARGET_MEASURE>`, `<MEASURE_TABLE>.MAX VALUE` — keep those aligned.

## Colors

| Token | Description | Example |
|---|---|---|
| `<POS_COLOR>` | Beat-target green (connector + label) | `#1B7F4A` |
| `<NEG_COLOR>` | Miss-target red | `#B00020` |
| `<NEUTRAL_COLOR>` | Within-tolerance grey ([tolerance variant](variants/tolerance-band-rag.md)) | `#9A9A9A` |

`<ACTUAL_FILL>` / `<TARGET_FILL>` use `ThemeDataColor` in the template (theme-driven); override with literals only if you must.

## IDs — generate fresh per build

| Token | Format | How |
|---|---|---|
| `<VISUAL_NAME_CHART>` | 20-char hex | `python -c "import uuid;print(uuid.uuid4().hex[:20])"` |
| `<*_LINEAGE_TAG>` | UUID | `python -c "import uuid;print(uuid.uuid4())"` |

Reuse the existing 20-hex `<PAGE_ID>` of the page you're adding the visual to.

## Layout

| Token | Description |
|---|---|
| `<CHART_X/Y/Z/HEIGHT/WIDTH/TAB_ORDER>` | Chart position + size |

## Bulk substitution

```bash
sed -i \
  -e "s/<MEASURE_TABLE>/Mesures/g" \
  -e "s/<ACTUAL_MEASURE>/NET SALES/g" \
  -e "s/<TARGET_MEASURE>/TARGET SALES/g" \
  -e "s/<AXIS_TABLE>/Dim_Date/g" \
  -e "s/<AXIS_COLUMN>/MoisCourt_2_en/g" \
  -e "s/<POS_COLOR>/#1B7F4A/g" \
  -e "s/<NEG_COLOR>/#B00020/g" \
  path/to/written/file
```
