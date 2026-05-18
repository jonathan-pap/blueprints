# QRY001 — Remove unneeded filters

> Tier 2 — explicit user approval required before applying.

Every filter adds a `WHERE` clause in xmSQL and may force an extra SE join. Users often apply global slicer or visual-level filters that don't actually affect the calculation being optimized.

## Detection

`WHERE` clauses on columns not used in the measure logic, or filter variables that restrict to a single value (e.g., `Currency[Code] = "USD"` in a USD-only model).

## Fix

Remove filters one at a time and re-run. If the result doesn't change, the filter might be unnecessary. Global filters that ARE needed across all visuals should be pushed to the data source (Tier 3 — see `../model-tuning/_index.md`).

## Example

```dax
-- Before: filter on Currency adds an SE join for no benefit
SUMMARIZECOLUMNS(
    'Product'[Category],
    KEEPFILTERS(TREATAS({"USD"}, 'Currency'[Code])),
    "Revenue", [Total Revenue]
)

-- After: filter removed, same result, one fewer SE join
SUMMARIZECOLUMNS('Product'[Category], "Revenue", [Total Revenue])
```

## Desktop action

In the Power BI Desktop UI, the user removes the slicer selection or visual-level filter. The agent suggests; the user implements via the report builder.
