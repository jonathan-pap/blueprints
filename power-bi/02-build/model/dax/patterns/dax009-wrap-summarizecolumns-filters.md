# DAX009 — Wrap SUMMARIZECOLUMNS filters with CALCULATETABLE

Filters passed as direct arguments to SUMMARIZECOLUMNS inside measures can produce unexpected results. Move filters to a wrapping CALCULATETABLE instead.

## Anti-pattern

```dax
SUMMARIZECOLUMNS(
    'Table'[Column],
    TREATAS({"Value"}, 'Table'[FilterColumn]),
    "@Calculation", [Measure]
)
```

## Preferred

```dax
CALCULATETABLE(
    SUMMARIZECOLUMNS(
        'Table'[Column],
        "@Calculation", [Measure]
    ),
    'Table'[FilterColumn] = "Value"
)
```

## Signal

Filter or `TREATAS` passed directly as `SUMMARIZECOLUMNS` argument (not wrapped in `CALCULATETABLE`).
