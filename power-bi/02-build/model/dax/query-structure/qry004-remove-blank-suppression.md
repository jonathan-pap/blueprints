# QRY004 — Remove BLANK suppression (changes result shape)

> Tier 2 — explicit user approval required before applying. **This pattern changes the result shape — gets a different number of rows.**

`+ 0`, `IF(ISBLANK([M]), 0, [M])`, or `COALESCE(..., 0)` force SUMMARIZECOLUMNS to evaluate every groupby combination — including rows with no data — inflating the result set.

## Detection

`+ 0`, `IF(ISBLANK(...))`, or `COALESCE(..., 0)` appended to measures.

## Anti-pattern

```dax
MEASURE 'Sales'[Revenue] = SUM('Sales'[SalesAmount]) + 0
```

## Preferred

```dax
MEASURE 'Sales'[Revenue] = SUM('Sales'[SalesAmount])
```

## If zeros are required selectively

Conditionally add 0 where it makes sense:

```dax
MEASURE 'Sales'[Revenue] =
    VAR _ForceZero = NOT ISEMPTY('Sales')
    RETURN [Sales Amount] + IF(_ForceZero, 0)
```

This forces zero only when at least one row exists for the current filter context, not for every empty combination.

## Trade-off

Removing blank suppression changes the visible row count in a matrix. Some users want to see all combinations (including zeros); others want to see only rows with data. Confirm the intent.
