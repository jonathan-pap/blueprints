# DL001 — V-Ordering for optimal VertiPaq compression

> Tier 4 — Direct Lake. User approval required. Requires Spark / ETL or Fabric resource profile changes.

Import models are always V-ordered. Direct Lake models are **not** — enable it explicitly.

V-ordering reorders rows within each rowgroup to maximize RLE compression (**2–5× improvement**).

## Two approaches

### Spark

```python
spark.conf.set("spark.microsoft.delta.vorder.enabled", "true")
# Then optimize the Delta table
spark.sql("OPTIMIZE my_table")
```

### Fabric resource profile

Use the [`readHeavyForPBI` resource profile](https://learn.microsoft.com/en-us/fabric/data-engineering/configure-resource-profile-configurations) which enables V-ordering and optimized write settings automatically.

```python
# Set the resource profile on the lakehouse
spark.conf.set("spark.fabric.resourceProfile", "readHeavyForPBI")
```

## Verify

After V-ordering, the Direct Lake model should show:

- Reduced VertiPaq memory footprint (check VertiPaq Analyzer)
- Faster cold-cache queries (less data to transcode)
- Better SE Parallelism Factor (segments compress to similar sizes)

## When to apply

- Any Direct Lake model where query perf matters
- Before promoting a DL model to production
- After significant data changes that would have de-optimized row order

## Cost

- Requires `OPTIMIZE` runs (which themselves require Spark compute)
- Slight write penalty during table updates (small relative to read benefit)

## See also

- `dl002-segment-size.md` — pair V-Ordering with right-sized rowgroups
- `../engine/compression.md` — why V-Ordering matters at the engine level
