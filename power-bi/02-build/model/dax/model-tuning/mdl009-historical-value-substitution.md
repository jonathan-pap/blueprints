# MDL009 — Cardinality reduction via historical value substitution

> Tier 3 — user approval required. Requires ETL / source change.

Replace old key values beyond a retention window with a single placeholder to collapse cardinality and shrink dictionaries. Can be done in both facts and dimensions.

## SQL pattern

```sql
CASE WHEN SaleDate >= DATEADD(year, -1, GETDATE())
     THEN SalesKey
     ELSE 'Historical Key'
END
```

All SalesKey values older than 1 year collapse to one value. Dictionary shrinks dramatically; queries on recent data still see full detail.

## When to use

- Long history with declining query relevance (10 years of data, 95 % of queries are last 90 days)
- Specific high-cardinality columns where users never drill into old detail (e.g., individual transaction IDs older than a year)
- Aggregation tables for old periods exist; detail is only needed for recent

## Trade-off

- **Loss of detail for historical periods** — irreversible at the model level (still in source)
- **Reporting against historical detail breaks** — confirm with stakeholders that this is acceptable
- **Refresh impact** — depends on whether the substitution is done at source or in Power Query

## Combine with

- Incremental refresh — old partitions are sealed, so the substitution stabilizes
- `mdl005-precompute-period-comparison.md` for fast YoY without TI scans
- `mdl003-data-types.md` for general cardinality reduction patterns

## When NOT to use

- Users do drill into historical detail (auditors, compliance, "what changed in 2020?")
- Compliance / regulatory requirement to retain detail
- Storage is cheap and the cardinality cost is tolerable
