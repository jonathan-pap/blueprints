# Fix: pick the right `formatString`

## Patterns by data type

- Integer: `#,##0` → `1,234`
- Decimal (2 places): `#,##0.00` → `1,234.56`
- Percentage (no decimals): `0%` → `85%`
- Percentage (1 decimal): `0.0%` → `85.0%`
- Currency USD: `$#,##0.00` → `$1,234.56`
- Currency EUR: `€#,##0.00` or `#,##0.00 €` → `€1,234.56`
- Date: `yyyy-MM-dd` → `2026-05-17`
- Date (US): `mm/dd/yyyy`
- Date (EU): `dd/mm/yyyy`
- Time: `HH:mm:ss`
- Variance: `+#,##0;-#,##0` (sign always shown)
- Variance %: `+0.0%;-0.0%`

## On the measure

```tmdl
measure 'Revenue' = SUM('Sales'[Amount])
    formatString: #,##0.00
    lineageTag: abc-123
```

## On the column

```tmdl
column 'Amount'
    dataType: double
    formatString: #,##0.00
    lineageTag: abc-123
    summarizeBy: sum
    sourceColumn: Amount
```

## When `formatString` doesn't apply

Some measures use `formatStringDefinition` instead (dynamic formats from DAX). See `dynamic-format-string.md`.

## Display-unit interaction

In a visual, the display unit (`Millions`, `Thousands`) interacts with the format string. Custom format strings often override the visual's "Auto" display unit, producing unrounded values. See `../../report/add-visual/kpi-card.md` for guidance.

## After

`bash ../../../04-review/hooks/validate-tmdl.sh "<project>.SemanticModel"`.
