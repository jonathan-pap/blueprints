# Add a calculated table (TMDL)

A table whose rows come from a DAX expression. No M, no source.

## File: `tables/Date.tmdl`

```tmdl
table 'Date'
    lineageTag: <generate-new-guid>
    dataCategory: Time

    partition 'Date-Partition' = calculated
        mode: import
        source = CALENDAR(DATE(2020,1,1), DATE(2030,12,31))
```

After refresh, the engine infers columns from the DAX expression. You can then declare them explicitly:

```tmdl
table 'Date'
    lineageTag: <guid>
    dataCategory: Time

    column 'Date'
        dataType: dateTime
        formatString: yyyy-MM-dd
        lineageTag: <guid>
        summarizeBy: none

    column 'Year'
        type: calculated
        dataType: int64
        lineageTag: <guid>
        summarizeBy: none
        expression: YEAR('Date'[Date])

    partition 'Date-Partition' = calculated
        mode: import
        source = CALENDAR(DATE(2020,1,1), DATE(2030,12,31))
```

## Then add to `model.tmdl`

```tmdl
ref table 'Date'
```

## Mark as date table

`dataCategory: Time` on the table + a date column. Then set the date column as the table's date key via the appropriate annotation (Power BI Desktop usually does this automatically once the data category is set).

## After

`bash ../../../04-review/hooks/validate-tmdl.sh "<project>.SemanticModel"`. Reopen Desktop and refresh.
