# QRY003 — Reduce query grain

> Tier 2 — explicit user approval required before applying.

Grouping by a high-cardinality column (e.g., `Calendar[Date]` → 365 rows) when the user only needs monthly data (12 rows) inflates SE row count ~30×.

## Detection

Groupby on a date or high-cardinality column producing far more rows than the visual needs.

## Four options

### Option A — coarser groupby

```dax
-- Daily → monthly
SUMMARIZECOLUMNS('Calendar'[YearMonth], "Revenue", [Total Revenue])
```

Desktop action: user changes the axis field from `Calendar[Date]` to `Calendar[YearMonth]`.

### Option B — period-end axis + measure pin

Requires a period-end column in the date table (e.g., `Calendar[MonthEndDate]`). User changes the visual axis to it, then the measure pins CALCULATE to that date:

```dax
-- User changes axis from Calendar[Date] to Calendar[MonthEndDate]
-- Measure pins CALCULATE to the period-end date to return that day's value only
MEASURE 'Sales'[Active Customers] =
    CALCULATE(
        DISTINCTCOUNT('Sales'[CustomerID]),
        'Calendar'[Date] = MAX('Calendar'[MonthEndDate])
    )
```

Without the pin, grouping by `MonthEndDate` aggregates all days in the month instead of returning the single-day value.

### Option C — return BLANK for non-boundary dates

Keeps all dates in groupby but only computes on end-of-month:

```dax
MEASURE 'Sales'[Revenue EOM] =
    IF(MAX('Calendar'[Date]) = EOMONTH(MAX('Calendar'[Date]), 0), [Total Revenue])
```

### Option D — daily additive measure approximated at coarser grain

Divide monthly total by days in month:

```dax
MEASURE 'Sales'[Daily Avg Revenue] =
    DIVIDE(
        [Total Revenue],
        DAY(EOMONTH(MAX('Calendar'[Date]), 0))
    )
```

## Trade-off

Each option changes what's displayed. Confirm with the user that the new result shape matches their analytical need before applying.
