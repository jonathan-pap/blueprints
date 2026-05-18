# Trace analysis — event types and what to look for

Trace events captured from Analysis Services during query execution. Each event has: `EventClass`, `EventSubclass`, `TextData` (xmSQL or DAX), `Duration`, `CpuTime`, `StartTime`, `EndTime`.

## Key event types

- **`VertiPaqSEQueryBegin` / `VertiPaqSEQueryEnd`** — SE scan lifecycle. `Duration` and `CpuTime` are on the End event. `TextData` contains the xmSQL.
- **`VertiPaqSEQueryCacheMatch`** — SE query answered from cache (no scan). Count separately.
- **`QueryBegin` / `QueryEnd`** — Overall DAX query lifecycle. `Duration` on `QueryEnd` = total wall-clock time.
- **`AggregateTableRewriteQuery`** — Fired when engine rewrites a query to use an aggregation table. `TextData` contains the rewritten query. Presence = agg table hit; absence on an agg-enabled model = query fell through to detail table.

## Filtering trace output

Focus on the event types above. Ignore:

- **`VertiPaqScanInternal` subclass events** — duplicate the outer `VertiPaqScan` with internal detail (e.g., `DC_KIND="DENSE"`) and identical timing
- **`CommandBegin` / `CommandEnd`** — DAX execution wrapper, no diagnostic value
- **`Error` events** — only relevant when errors occur

## Building an FE gap waterfall

FE processing occurs in the gaps **between** SE events. Use `StartTime` / `EndTime` offsets from `QueryBegin.StartTime` to build a timeline:

1. Gap between `QueryBegin` and first SE `StartTime` → **FE plan compilation**
2. Gap between one SE `EndTime` and next SE `StartTime` → **FE processing block**
3. Gap between last SE `EndTime` and `QueryEnd.EndTime` → **final FE assembly**
4. Overlapping SE events → parallel SE execution; sequential non-overlapping → FE feeding results between scans
5. **A large gap (> 100 ms) signals expensive FE computation** — examine the SE query *before* the gap

## What to look for (priority order)

Scan for these signals when analyzing a slow query:

1. **Callbacks** — `CallbackDataID` or `EncodeCallback` in SE TextData. Fix first (DAX002, DAX007, DAX008, DAX018).
2. **High FE %** — FE doing too much work; usually paired with many short SE queries.
3. **High SE query count / repeated fact scans** — multiple SE queries hitting same fact table with same joins but different WHERE clauses or aggregations → **blocked fusion**. See `fusion.md`.
4. **Large materializations** — SE rows far exceed final result, or SE queries with no WHERE clause → FE filtering post-materialization instead of pushing to SE. See DAX009.
5. **Low parallelism factor** — near 1.0 on slow scans → **data layout problem**, not DAX. See `compression.md`.
6. **High KB per SE event** — wide intermediate tables; reduce columns or aggregate earlier.
7. **Two-step dimension pre-scans** — dimension-only SELECT followed by `where predicate` on fact. Restructure query to collapse into one scan.
8. **Large semi-join index tables** — `DEFINE TABLE` + `ININDEX` or `WHERE ... IN` with hundreds of compound tuples. See DAX021.
9. **Missing aggregate table hit** — Model has agg tables configured but no `AggregateTableRewriteQuery` event → query fell through to detail. Check agg mappings and query grain.

## Prioritization

Callbacks → Large FE processing → SE query count (DAX) → parallelism and data volume (data layout).

**Target the highest-duration SE scan first.** Ignore 0 ms cache-hit scans.

## See also

- `xmsql.md` — interpreting `TextData`
- `trace-metrics.md` — deriving the metrics referenced here
- `dax-vs-data-layout.md` — telling DAX problems from data layout problems
- `../decision-guide.md` — signal → pattern mapping
