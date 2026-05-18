# Compression, segments, and parallelism

VertiPaq's columnar storage determines SE scan speed. Three levers: encoding, segments, V-ordering.

## Compression

VertiPaq uses two encodings:

- **Run-length encoding (RLE)** — sequences of identical values stored as `(value, count)`. Effective when values cluster.
- **Dictionary encoding** — distinct values stored once; rows store dictionary IDs. Effective for low-to-mid cardinality.

**V-ordering** reorders rows within segments to maximize RLE compression.

- **Import models are V-ordered automatically.**
- **Direct Lake models are NOT** — enable V-ordering explicitly. See `../model-tuning/dl001-v-ordering.md`.

## Segments

Segments are fixed-size column chunks — the unit of both compression and parallel execution. The SE assigns **one CPU thread per segment**, so segment count determines how many cores a scan can utilize.

### Target segment count

Aim for **1–16 M rows per segment**. Below 1 M, segment overhead exceeds work. Above 16 M, parallelism drops.

### Skew matters

If one segment has 15 M rows and the rest have 1 M each, the scan bottlenecks on the oversized segment. Even sizing is as important as segment count.

## Parallelism

A 32 M-row table in 2 segments → 2 threads. Same table in 32 segments → all 16 available threads → 4–8× speedup with **zero DAX changes**.

## Diagnosing low parallelism

**SE Parallelism Factor** = `StorageEngineCpuTime ÷ StorageEngineDuration`.

- Near 1.0 → single-threaded execution
- 8–16 → strong multi-core use

When a trace shows:

- Few SE queries (1–4)
- High SE Duration
- Parallelism Factor ≈ 1.0
- Clean xmSQL (no callbacks, no large materializations)

…the bottleneck is **too few segments or skewed segment sizes**. This cannot be fixed with DAX — the fix is data layout.

See `../model-tuning/_index.md` "General Data Layout Best Practices" and `../model-tuning/dl001-v-ordering.md` / `dl002-segment-size.md` for Direct Lake.

## See also

- `architecture.md` — FE vs SE
- `fusion.md` — how multiple scans get merged
- `trace-metrics.md` — Parallelism Factor derivation
- `dax-vs-data-layout.md` — when DAX changes apply vs data layout changes
