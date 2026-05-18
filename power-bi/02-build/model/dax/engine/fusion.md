# SE query fusion

Fusion is the engine's ability to combine multiple SE scans into fewer scans. **Critical for performance** — N independent scans usually take ~N× as long as one fused scan.

Two types: vertical and horizontal.

## Vertical fusion

Merges multiple measure aggregations that share the same filter context into a single SE query.

Three measures on the same fact table under the same filter → **one scan instead of three**. Gain scales with fact table size.

### What blocks vertical fusion

- **Time intelligence functions** (DATESYTD, DATEADD, SAMEPERIODLASTYEAR, etc.) — each TI-modified measure needs its own date-filtered SE scan. Fix → `../patterns/dax019-vertical-fusion-ti.md`
- **Per-measure filter predicates** — can cause the FE to materialize separate `VAND` tuple predicates per measure, producing structurally different SE queries even when underlying logic is identical. Fix → `../patterns/dax017-boolean-multiplier.md`
- **SWITCH / IF selecting between measures** — engine cannot determine at plan time which aggregation to include
- **Calculation group items** applying different filter modifications — each generates its own SE query

## Horizontal fusion

Merges SE queries that differ only in which single value of a column they filter. N separate fact scans collapse to one; the FE partitions the result.

### What blocks horizontal fusion

- **Filtered column not in groupby** — engine cannot merge slices if the slicing column is absent
- **Table-valued filter per measure** (e.g., time intelligence) — prevents slice merging even when column filters are identical
- **Filter value computed at runtime** (stored in a variable) — engine treats as dynamic and will not fuse

Fix → `../patterns/dax020-horizontal-fusion.md` and `dax017-boolean-multiplier.md`.

## Trace diagnosis

- **Multiple SE queries hitting same fact table with same joins** → vertical fusion blocked
- **N near-identical SE queries with only WHERE filter differing** → horizontal fusion blocked

See `trace-analysis.md` for the full diagnostic flow.

## See also

- `architecture.md` — FE vs SE
- `trace-metrics.md` — SE Query Count metric (lower is better)
- `../patterns/dax017-boolean-multiplier.md`, `dax019-vertical-fusion-ti.md`, `dax020-horizontal-fusion.md` — the fixes
