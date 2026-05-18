# Trace metrics — FE vs SE derivation

Critical metrics for DAX optimization, derived from Analysis Services trace events.

## Core metrics

| Metric | How to derive | Description | Target |
|---|---|---|---|
| **Total Duration** | `QueryEnd.Duration` | End-to-end query time (ms) | Lower is better |
| **FE Duration** | Total Duration − SE wall-clock time | Single-threaded FE processing time (ms) — **the #1 bottleneck in most slow queries** | Lower is better |
| **SE Duration** | Union of overlapping `VertiPaqSEQueryEnd` intervals | Multi-threaded SE query time (ms) | Higher % of total is better |
| **SE Query Count** | Count of `VertiPaqSEQueryEnd` events | Number of SE scans generated | Fewer is better |
| **SE CPU Time** | Sum of all `VertiPaqSEQueryEnd.CpuTime` | Total CPU across all SE threads | Higher ratio to SE Duration is better |
| **SE Parallelism Factor** | SE CPU Time ÷ SE Duration | Thread utilization across all scans | Higher is better (>1 = multi-threaded) |
| **Cache Matches** | Count of `VertiPaqSEQueryCacheMatch` events | SE queries answered from memory | Only relevant on warm cache |
| **Peak Memory (KB)** | From execution metrics summary | Memory consumed during execution | Lower is better — high values signal excessive materializations |
| **SE Scan Row Count** | `volume` from `[Estimated size (volume, marshalling bytes): X, Y]` in `VertiPaqSEQueryEnd.TextData` | Rows materialized per SE scan | Large volumes signal excessive materialization |
| **FE %** | FE Duration ÷ Total Duration × 100 | Percentage of time in formula engine | Lower is better |
| **SE %** | SE Duration ÷ Total Duration × 100 | Percentage of time in storage engine | Higher is better |

## Important nuances

### Net wall-clock for SE Duration

SE Duration is the **union** of overlapping SE intervals — NOT the sum of individual durations.

Three concurrent 100 ms scans = ~100 ms wall clock, not 300 ms.

### Parallelism — aggregate vs per-scan

The aggregate parallelism factor is computed across all SE scans. Each individual scan has its own `CpuTime / Duration`.

A healthy aggregate factor can mask a single unparallelized scan where `CpuTime ≈ Duration`. Always inspect per-scan parallelism for slow scans.

### FE processing gaps

FE Duration is the sum of all time intervals where **no SE query was executing** — gaps between SE events on the timeline.

See `trace-analysis.md` for building an FE gap waterfall from `StartTime`/`EndTime` offsets.

## Per-scan derived metrics (from `VertiPaqSEQueryEnd`)

Each `VertiPaqSEQueryEnd` event provides raw data to derive per-scan diagnostics:

- **Rows scanned / Marshalling KB** — parse `[Estimated size (volume, marshalling bytes): X, Y]` at the end of `TextData`. X = rows, Y = bytes. Identifies excessive materializations on a specific scan.
- **Per-scan parallelism** — `CpuTime / Duration` for that individual scan. Ratio near 1.0 means single-threaded even if aggregate looks healthy.
- **Callbacks on slow scans** — scan `TextData` for `CallbackDataID` / `EncodeCallback` to confirm which specific SE query has the callback.

## See also

- `architecture.md` — FE vs SE
- `xmsql.md` — what's in `TextData`
- `trace-analysis.md` — event types + what-to-look-for + FE gap waterfall
- `compression.md` — Parallelism Factor and what drives it
