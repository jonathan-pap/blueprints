# DL002 — Segment size and parallelism

> Tier 4 — Direct Lake. User approval required.

Delta rowgroups map directly to VertiPaq segments — **one segment per CPU core**. More segments = better CPU saturation (see SE Parallelism Factor in `../engine/compression.md`).

## Target: 1–16 M rows per rowgroup

- **Too few rowgroups** → single-threaded scans
- **Too many tiny rowgroups** → merge overhead dominates

For small tables (< 1 M rows) this rarely matters.

## OPTIMIZE regularly

Run `OPTIMIZE` to consolidate small files into properly sized rowgroups:

```sql
OPTIMIZE my_table
```

In Fabric: typically scheduled as a maintenance job or wired into ETL pipelines.

## Match capacity SKU to table size

Maximize available cores by choosing a capacity SKU that matches table size — a table with 2 segments on an F64 wastes most of its parallelism budget.

| Table size | Recommended rowgroup count | Implied capacity SKU |
|---|---|---|
| < 1 M rows | 1–2 segments | Any |
| 1–16 M | 2–4 segments | F4+ |
| 16–256 M | 8–16 segments | F32+ |
| 256 M–1 B | 16–32 segments | F64+ |
| > 1 B | 32+ segments + partitioning | F256+ |

## Verify

In `../engine/trace-metrics.md`, look at SE Parallelism Factor for queries against the DL table:

- Near 1.0 → single-threaded scans (segment count too low or skewed)
- 8–16 → strong multi-core use (target achieved)

## Symptoms of segment problems

- Cold-cache queries disproportionately slow
- SE Parallelism Factor ≈ 1.0 on individual scans
- Few SE queries, high duration, clean xmSQL (no callbacks)

Per `../engine/dax-vs-data-layout.md`: this signal pattern means **data layout**, not DAX. Fix at the Delta layer.

## See also

- `dl001-v-ordering.md` — pair V-Ordering with right-sized rowgroups
- `../engine/compression.md` — segments and parallelism mechanics
