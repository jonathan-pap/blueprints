# Formula Engine vs Storage Engine

Every DAX query runs through two components: the **Formula Engine (FE)** and the **Storage Engine (SE)**.

## FE — single-threaded; the bottleneck

Handles all DAX semantics: branching logic, context transitions, complex arithmetic, measure evaluation. **Single-threaded.** The bottleneck in most poorly written queries.

## SE — multi-threaded; fast but limited

Reads compressed columnar data from VertiPaq. **Multi-threaded.** Very fast but supports only:

- Four basic arithmetic operators
- GROUP BY
- LEFT OUTER JOINs
- Basic aggregations (SUM, COUNT, MIN, MAX, DISTINCTCOUNT)

For **DirectQuery models**, the SE role is played by the underlying data source (SQL, Spark, etc.). FE generates SQL and pushes it down. Trade-off: network and source latency instead of in-memory scan cost.

## How they interact

The FE requests data from the SE in one or more scans — each result is a **datacache** (set of columns + aggregated values). Complex queries may require multiple datacaches: one to build a filter set, another to aggregate the fact.

When the SE cannot evaluate an expression natively, it **calls back** to the FE row-by-row — making that SE scan effectively single-threaded.

## The optimization principle

**Push as much work as possible into the SE, minimize SE scans, eliminate callbacks entirely.**

Every DAX optimization pattern in `../patterns/` follows this principle.

## Why callbacks matter

A callback happens when SE encounters an expression VertiPaq can't evaluate (conditional logic, custom functions). The SE pauses, calls back to the FE per row, then continues. Effectively single-threaded; defeats the SE's multi-core advantage.

Common culprits:

- `IF()` inside iterators → DAX007
- Context transitions inside iterators → DAX008
- `DIVIDE()` inside iterators → DAX018
- Custom DAX functions (UDFs) inside iterators

Fix: replace with SE-native equivalents. See `../decision-guide.md` for signal-to-pattern mapping.

## See also

- `xmsql.md` — what SE scan activity looks like in traces
- `compression.md` — how SE achieves multi-thread speed
- `fusion.md` — how SE scans get merged
- `trace-metrics.md` — how to measure FE vs SE in your own traces
