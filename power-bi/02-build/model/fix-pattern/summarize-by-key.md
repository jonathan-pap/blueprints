# Fix: key column wrongly summing

## Symptom

A key column (e.g. `CustomerID`) is set to `summarizeBy: sum`. Power BI tries to aggregate it when dragged into a visual, producing nonsense ("Sum of CustomerID = 384,927").

## Fix

```tmdl
# Before
column 'CustomerID'
    dataType: int64
    isHidden
    lineageTag: abc-123
    summarizeBy: sum                ← wrong
    sourceColumn: CustomerID

# After
column 'CustomerID'
    dataType: int64
    isHidden
    lineageTag: abc-123
    summarizeBy: none               ← correct
    sourceColumn: CustomerID
```

## Rule of thumb

| Column kind | `summarizeBy` |
| --- | --- |
| Keys (surrogate / natural) | `none` |
| Attributes (names, codes, types) | `none` |
| Dates | `none` |
| Boolean flags | `none` |
| Additive numeric facts (amounts, quantities) | `sum` |
| Non-additive facts (rates, percentages) | `none` (cannot be meaningfully summed) |

## Find all candidates

```bash
grep -rE "summarizeBy: sum" "<project>.SemanticModel/definition/tables/" | grep -iE "(id|key|code)"
```

Then audit each — keys/codes should be `none`.

## After

`bash ../../../04-review/hooks/validate-tmdl.sh "<project>.SemanticModel"`.
