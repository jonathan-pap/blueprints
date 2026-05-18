# Add a measure (TMDL)

Edit `<project>.SemanticModel/definition/tables/<table>.tmdl`. Place inside the `table` block at depth 1.

## Single-line DAX

```tmdl
measure 'Total Revenue' = SUM('Sales'[Amount])
    formatString: #,##0
    displayFolder: 1. Revenue
    lineageTag: <generate-new-guid>
```

## Multi-line DAX (indented block)

DAX body is 2 levels deeper than the declaration:

```tmdl
measure 'Actuals MTD' =
        CALCULATE(
            [Actuals],
            CALCULATETABLE(
                DATESMTD('Date'[Date]),
                'Date'[IsDateInScope]
            )
        )
    formatString: #,##0
    displayFolder: 2. MTD\Actuals
    lineageTag: <generate-new-guid>
```

## With description

```tmdl
/// Sum of Sales[Amount] in the current filter context.
measure 'Total Revenue' = SUM('Sales'[Amount])
    formatString: #,##0
    lineageTag: <generate-new-guid>
```

## Dynamic format

```tmdl
measure 'Variance %' = DIVIDE([Variance], [Target])
    displayFolder: 3. Variance
    lineageTag: <generate-new-guid>

    formatStringDefinition =
            IF([Variance] < 0, "-0.0%;0.0%", "+0.0%;0.0%")
```

## After

- `lineageTag`: use any unique GUID for a new object. Tools like `uuidgen` work.
- Validate: `bash ../../../04-review/hooks/validate-tmdl.sh "<project>.SemanticModel"`.
- Reopen Power BI Desktop (it doesn't detect external edits).
