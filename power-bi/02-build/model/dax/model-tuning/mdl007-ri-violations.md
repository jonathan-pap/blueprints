# MDL007 — Eliminate referential integrity violations

> Tier 3 — user approval required. Requires source-side data fix or ETL handling.

Fact FKs with no matching dimension row prevent inner-join rewriting for SWITCH / multi-measure patterns. The engine has to use LEFT OUTER joins (and handle the BLANK side) instead of cheaper INNER joins.

## Detection

```dax
SELECT [Dimension_Name], [RIVIOLATION_COUNT]
FROM $SYSTEM.DISCOVER_STORAGE_TABLES
WHERE [RIVIOLATION_COUNT] > 0
```

Returns the dimensions with orphaned fact FKs (Fact has a key value the Dim doesn't have).

## Fix

Add an "Unknown" catch-all row to each affected dimension. In ETL or Power Query:

```sql
-- Catch-all row
INSERT INTO Dim (Key, Name, ...) VALUES (-1, 'Unknown', ...)
```

Then map missing foreign keys in fact to the `-1` placeholder:

```sql
UPDATE Fact
SET DimKey = -1
WHERE DimKey NOT IN (SELECT Key FROM Dim)
```

After both: zero RI violations, engine can use INNER joins, SWITCH and multi-measure patterns become cheaper.

## Trade-off

- Permanently keeps an "Unknown" row visible in slicers — design choice (hide it via the dim's display setting, or show it as a known-bad indicator)
- Requires writeable source or Power Query enforcement
- Doesn't always help small models — the overhead is more visible on large facts with many SWITCH measures

## When NOT to bother

- Small models (< 1 M fact rows) — overhead is negligible
- No SWITCH / multi-measure patterns in the model
