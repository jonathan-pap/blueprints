# MDL003 — Column cardinality and data type optimization

> Tier 3 — user approval required.

High-cardinality columns inflate dictionary size and segment memory.

## Patterns

### Integer keys over string keys

Replace `"PROD-001234"` with integer surrogates. String keys cost ~10× more in dictionary size for the same cardinality.

### Reduce timestamp precision

`DateTime` → `Date` when queries only group by date.

Splitting `DateTime` into separate `Date` + `Time` columns achieves 90 %+ memory reduction when queries only need date-level filters.

### Bin continuous values

50K distinct decimals → binned ranges (e.g., 50 buckets) if measure logic allows. Trade fidelity for compression.

### Split high-cardinality columns

`FullAddress` (100K distinct) → `City`, `State`, `Zip` (each low cardinality individually).

The split tables compress better and most queries only need one or two components — they don't load all the high-cardinality detail.

## Decision flow

1. Run VertiPaq Analyzer to find the largest columns by memory.
2. For each: ask "do queries actually need this fidelity?"
3. If no → reduce precision or split.
4. If yes → it's intrinsic; look at other patterns (MDL004 aggregations).

## See also

- `../../object-types/column-properties.md` — data type enum values
- `../../fix-pattern/summarize-by-key.md` — `summarizeBy: none` on key columns prevents wrong-sum bugs
- `../../../../04-review/model-audit/performance.md` — VertiPaq Analyzer workflow
