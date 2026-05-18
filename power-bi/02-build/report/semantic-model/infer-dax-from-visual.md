# Infer the DAX a visual is generating

Power BI generates a DAX `SUMMARIZECOLUMNS` query per visual at runtime. You can reconstruct it from the visual JSON.

## Read the bindings

```bash
pbir visuals bind "<...>/Visual.Visual" --show
```

Output lists each role + bound field.

## Map to DAX

For a bar chart bound `Category: Geography.Region`, `Y: Sales.Revenue`:

```dax
EVALUATE
SUMMARIZECOLUMNS(
    'Geography'[Region],
    "Revenue", [Revenue]
)
ORDER BY [Revenue] DESC
```

For a matrix with multiple `Rows` and `Columns`, each becomes a grouping key in `SUMMARIZECOLUMNS`.

## Filters become CALCULATETABLE wrappers

Page filters and visual filters wrap the query:

```dax
EVALUATE
CALCULATETABLE(
    SUMMARIZECOLUMNS(...),
    'Date'[Calendar Year] = 2026
)
```

## To capture the exact runtime query

Use the live trace: `../../../03-bind/references/query-listener.md`. The trace shows the actual DAX with all filter context applied.
