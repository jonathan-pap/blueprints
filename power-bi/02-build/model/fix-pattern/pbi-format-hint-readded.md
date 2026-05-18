# Fix: `PBI_FormatHint` keeps coming back

## Symptom

You remove a `PBI_FormatHint` annotation from a column. Next time Power BI Desktop saves, it's back.

## Cause

Power BI Desktop manages this annotation automatically. Setting a `formatString` triggers Desktop to compute and write a matching `PBI_FormatHint`. The annotation hints at what kind of value the format string is producing (general number, percentage, currency, etc.).

## Resolution

**Don't fight it. Leave the annotation in place.** It does no harm; removing it just creates churn on every save.

## Example

```tmdl
column 'Amount'
    dataType: decimal
    formatString: #,##0.00
    lineageTag: abc-123
    summarizeBy: sum
    sourceColumn: Amount

    annotation SummarizationSetBy = Automatic

    annotation PBI_FormatHint = {"isGeneralNumber":true}    ← leave this
```

## When is it set

- Setting `formatString` on a column → Desktop adds or updates `PBI_FormatHint`.
- Setting a percentage format like `0.0%` → `PBI_FormatHint = {"isPercentage":true}`.
- Setting a currency format → `PBI_FormatHint = {"currencyCulture":"..."}`.

## Suppress entirely

Not recommended. If you really must:

- Remove the column's `formatString:` entirely (Desktop won't add a hint without one).
- Or set the format from a calculation group via `formatStringDefinition` (different code path; doesn't trigger the hint).
