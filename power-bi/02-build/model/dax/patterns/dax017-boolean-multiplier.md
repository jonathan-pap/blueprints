# DAX017 — Apply boolean multiplier to unblock fusion

**SE signal:** Near-identical SE queries on the same fact table that differ only by a column filter value or by per-measure `VAND` tuple predicates on the same column.

**Fix:** Replace the per-measure filter with `SUMX(KEEPFILTERS(ALL(Column)), expr * boolean)` to move the filter from SE to FE, making SE queries structurally identical across measures.

## Anti-pattern — separate SE query per measure

```dax
CALCULATE(SUM('Sales'[Amount]), 'Product'[Category] = "Bikes")
CALCULATE(SUM('Sales'[Amount]), 'Date'[Date] = _dateAnchor)
CALCULATE(MAX('Sales'[DateKey]), 'Sales'[Metric] <> 0)
```

## Preferred — boolean multiplier; structurally identical SE queries → engine fuses

```dax
SUMX(KEEPFILTERS(ALL('Product'[Category])), CALCULATE(SUM('Sales'[Amount])) * ('Product'[Category] = "Bikes"))
SUMX(KEEPFILTERS(ALL('Date'[Date])),        CALCULATE(SUM('Sales'[Amount])) * ('Date'[Date] = _dateAnchor))
MAXX(ALL('Date'[Date]),                     CALCULATE(MAX('Sales'[DateKey])) * INT(NOT ISBLANK(CALCULATE(SUM('Sales'[Metric])))))
```

## Why it works

`KEEPFILTERS` preserves external context. When the column is in the groupby, detail cells iterate only 1 row. Works with all aggregation types.

## BLANK → 0 caveat

The boolean pattern returns 0 instead of BLANK when no data exists. If `ISBLANK()` checks matter downstream, wrap:

```dax
VAR _r = SUMX(...) RETURN IF(_r = 0, BLANK(), _r)
```

## See also

- `../engine/fusion.md` — vertical and horizontal fusion mechanics
- `dax019-vertical-fusion-ti.md` and `dax020-horizontal-fusion.md` — other fusion patterns
