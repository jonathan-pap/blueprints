# Add a hierarchy (TMDL)

A drill path of levels, each pointing at a column. Lives inside the table block.

## Pattern

```tmdl
table 'Date'
    ...

    hierarchy 'Calendar'
        lineageTag: <generate-new-guid>

        level 'Year'
            lineageTag: <guid>
            column: 'Year'

        level 'Quarter'
            lineageTag: <guid>
            column: 'Quarter'

        level 'Month'
            lineageTag: <guid>
            column: 'Month'
```

## Rules

- `level` blocks belong inside `hierarchy`, not directly under `table`.
- Level order in the file = drill order in Desktop.
- Each `level` references a column on the **same table**.
- Each `level` needs its own `lineageTag`.

## With description

```tmdl
/// Drill from year down to day for time-series analysis.
hierarchy 'Calendar'
    lineageTag: <guid>
    ...
```

## After

`bash ../../../04-review/hooks/validate-tmdl.sh "<project>.SemanticModel"`. Reopen Desktop.
