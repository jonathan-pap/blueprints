# DAX020 — Unblock horizontal fusion by lifting filters

Horizontal fusion merges SE queries that differ only by column-slice filter. It breaks when the filtered column is missing from groupby, or when table-valued / runtime-computed filters are applied per measure.

**Fix:** Keep only simple column-slice filters inside base measures; lift everything else (TI, dynamic variables) to an outer CALCULATE.

## Anti-pattern — TI inside each slice measure (no fusion)

```dax
MEASURE 'Sales'[Bikes YTD]       = CALCULATE(SUM('Sales'[Amount]), 'Product'[Category] = "Bikes",       DATESYTD('Date'[Date]))
MEASURE 'Sales'[Accessories YTD] = CALCULATE(SUM('Sales'[Amount]), 'Product'[Category] = "Accessories", DATESYTD('Date'[Date]))
```

## Preferred — slice measures fuse, TI applied once

```dax
MEASURE 'Sales'[Bikes]       = CALCULATE(SUM('Sales'[Amount]), 'Product'[Category] = "Bikes")
MEASURE 'Sales'[Accessories] = CALCULATE(SUM('Sales'[Amount]), 'Product'[Category] = "Accessories")
MEASURE 'Sales'[Combined YTD] = CALCULATE([Bikes] + [Accessories], DATESYTD('Date'[Date]))
```

## Runtime variable filters

Same principle — move runtime variable filters to the consuming measure, not into each slice.

## When the filtered column is not in groupby

See `dax017-boolean-multiplier.md` for the boolean-multiplier workaround.

## Signal

Multiple SE queries hitting same fact table with WHERE clauses that differ only by single column value.
