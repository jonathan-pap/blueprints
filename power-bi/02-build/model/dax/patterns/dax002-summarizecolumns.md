# DAX002 — Replace ADDCOLUMNS/SUMMARIZE with SUMMARIZECOLUMNS

SUMMARIZECOLUMNS defines grouping + calculation in one step, enabling better SE fusion. Replace all ADDCOLUMNS / SUMMARIZE patterns.

## Anti-patterns

```dax
SUMMARIZE('Sales', 'Sales'[ProductKey], "Total Profit", [Profit])
ADDCOLUMNS(SUMMARIZE('Sales', 'Sales'[ProductKey]), "Total Profit", [Profit])
ADDCOLUMNS('Sales', "Total Profit", CALCULATE([Profit]))
ADDCOLUMNS(VALUES('Sales'[ProductKey]), "Total Profit", [Profit])
```

## Preferred

```dax
SUMMARIZECOLUMNS('Sales'[ProductKey], "Total Profit", [Profit])
```

## Signal

`ADDCOLUMNS` or `SUMMARIZE` in measure expression. CallbackDataID often shows up alongside.
