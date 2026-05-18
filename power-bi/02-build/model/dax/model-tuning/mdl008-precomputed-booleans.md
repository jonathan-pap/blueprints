# MDL008 — Replace SEARCH/FIND filters with pre-computed boolean columns

> Tier 3 — user approval required. Requires Power Query or ETL column addition.

`SEARCH()` / `FIND()` in filters forces row-by-row string scanning. Pre-compute the result as a boolean column (cardinality 2, ~1 bit/row) for pure columnar access.

Generalizes to any fixed-value logical test — date flags, category indicators, prefix checks.

## Anti-pattern (in measure or filter)

```dax
CALCULATE([Revenue], SEARCH("Premium", 'Product'[Description], 1, 0) > 0)
```

Every query row-scans `Description` strings looking for "Premium".

## Preferred — pre-compute the boolean

In Power Query:

```m
#"Premium Flag" = Table.AddColumn(
    Source,
    "Is Premium",
    each Text.Contains([Description], "Premium"),
    type logical
)
```

Then:

```dax
CALCULATE([Revenue], 'Product'[Is Premium] = TRUE)
```

The boolean column compresses to ~1 bit per row and filters via a dictionary lookup, not a string scan.

## Generalize the pattern

Any fixed logical test that's expensive at query time but cheap once:

- Date flags: `Is Weekend`, `Is Month End`, `Is Holiday`
- Category indicators: `Is Active Customer`, `Is High Value`
- Prefix / substring checks: `Starts With "INV-"`, `Contains "REFUND"`

## Trade-off

- New column per test — model widens slightly
- Each new flag adds a Power Query step (or a source view column)
- Trades CPU at query time for storage + refresh cost (much better trade)

## See also

- `../../update/property.md` — adding columns to TMDL
- Power Query column patterns → `../../power-query/best-practices/_index.md`
