# Add a calculation group (TMDL)

A calculation group is a special table that swaps the applied calculation context for any measure. Common use: time intelligence (`YTD`, `MTD`, `PY`, `YoY %`).

## Pattern

```tmdl
table 'Time Intelligence'
    lineageTag: <generate-new-guid>

    calculationGroup
        precedence: 10

        calculationItem 'Current' = SELECTEDMEASURE()
        calculationItem 'YTD'     = CALCULATE(SELECTEDMEASURE(), DATESYTD('Date'[Date]))
        calculationItem 'MTD'     = CALCULATE(SELECTEDMEASURE(), DATESMTD('Date'[Date]))
        calculationItem 'PY'      = CALCULATE(SELECTEDMEASURE(), SAMEPERIODLASTYEAR('Date'[Date]))
        calculationItem 'YoY %'   = DIVIDE([Current] - [PY], [PY])

    column 'Time Calculation'
        dataType: string
        lineageTag: <guid>
        summarizeBy: none
        sourceColumn: Name

    partition 'Time Intelligence-Partition' = calculated
        mode: import
        source = {("Current", 0), ("YTD", 1), ("MTD", 2), ("PY", 3), ("YoY %", 4)}
```

## Required pieces

- A regular `table` declaration.
- A `calculationGroup` block (replaces normal table content).
- `calculationItem` blocks — the DAX swaps that get applied.
- A `column` that exposes the item names — bind this to slicers.
- A calculated `partition` whose source produces the (name, ordinal) pairs.

## Then add to `model.tmdl`

```tmdl
ref table 'Time Intelligence'
```

## Precedence

If you have multiple calculation groups (e.g. Time + Currency), `precedence:` controls application order. Higher number applies first. Common: time = 10, currency = 5.

## After

`bash ../../../04-review/hooks/validate-tmdl.sh "<project>.SemanticModel"`. In Desktop, drop the calculation-group column onto a slicer or table to swap measure context.
