# Tokens

Substitute every `<TOKEN>` across the [templates](templates/) before writing files.
The base recipe only has *report* tokens (it's visual-calc only); the model tokens apply
to the [model-measure variant](variants/model-measure-pareto.md).

## Data binding (the only ones you must change)

| Token | Description | Example |
|---|---|---|
| `<CATEGORY_TABLE>` | Table holding the dimension on the axis | `02: Product` |
| `<CATEGORY_COLUMN>` | The category column (the bars) | `Product` |
| `<MEASURE_TABLE>` | Table holding the value measure | `00: Calculations` |
| `<VALUE_MEASURE>` | Measure to rank + accumulate | `Sold $` |
| `<THRESHOLD>` | Pareto cutoff as a fraction. In JSON literals it carries a `D` suffix → `<THRESHOLD>D` | `0.8` (→ `0.8D`) |

## Internal names (fixed — rename only in lockstep)

These are the recipe's own visual-calculation names. They're referenced *by name* inside
other expressions and in formatting selectors, so leave them as shipped unless you rename
every reference together.

| Name | Role |
|---|---|
| `Percent of grand total` | P2 share-of-total (hidden) |
| `Pareto` | P3 naive cumulative (hidden — kept as the "before") |
| `Easy Pareto` | P3 sort-independent cumulative (the shown line) |
| `GreenLine` / `RedLine` | P4 line split at the threshold |

The line-series formatting selectors key off the **queryRef aliases** `select`, `select1`,
`select2`, `select3`, `select4` (= share, Pareto, Easy Pareto, GreenLine, RedLine). Keep
those aliases aligned with the projection order — the conditional fill references `select2`.

## Colors

| Token | Description | Example |
|---|---|---|
| `<VITAL_COLOR>` | "Vital few" — line + bars ≤ threshold | `#1E9790` (teal) |
| `<TRIVIAL_COLOR>` | "Trivial many" — line + bars > threshold | `#ED4D55` (red) |
| `<VITAL_LABEL_COLOR>` | Data-label tint on the green segment | `#C1DEC1` |
| `<TRIVIAL_LABEL_COLOR>` | Data-label tint on the red segment | `#efb5b9` |

## IDs — generate fresh per build

| Token | Format | How |
|---|---|---|
| `<VISUAL_NAME_CHART>` | 20-char hex | `python -c "import uuid;print(uuid.uuid4().hex[:20])"` |
| `<RANK_LINEAGE_TAG>` / `<CUM_LINEAGE_TAG>` (model variant) | UUID | `python -c "import uuid;print(uuid.uuid4())"` |

Reuse the existing 20-hex `<PAGE_ID>` folder of the page you're adding the visual to.

## Layout

| Token | Description |
|---|---|
| `<CHART_X/Y/Z/HEIGHT/WIDTH/TAB_ORDER>` | Chart position + size |

## Model tokens (model-measure variant only)

| Token | Description | Example |
|---|---|---|
| `<CUM_MEASURE_NAME>` | Cumulative measure name | `Cumulative %` |
| `<RANK_COLUMN_NAME>` | Rank calculated-column name | `Value Rank` |

## Bulk substitution

```bash
# after copying templates/pareto-combo.visual.json to its destination
sed -i \
  -e "s/<CATEGORY_TABLE>/02: Product/g" \
  -e "s/<CATEGORY_COLUMN>/Product/g" \
  -e "s/<MEASURE_TABLE>/00: Calculations/g" \
  -e "s/<VALUE_MEASURE>/Sold \$/g" \
  -e "s/<VITAL_COLOR>/#1E9790/g" \
  -e "s/<TRIVIAL_COLOR>/#ED4D55/g" \
  -e "s/<THRESHOLD>/0.8/g" \
  path/to/written/visual.json
```

> The threshold sed turns `<THRESHOLD>D` into `0.8D` (JSON) and `<THRESHOLD>` into `0.8`
> (DAX) in one pass — both forms share the `<THRESHOLD>` token.
