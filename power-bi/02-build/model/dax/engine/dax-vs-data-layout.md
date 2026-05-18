# DAX problem vs data layout problem

Reading the trace signal to decide where to fix.

## Signal: Many SE queries + high FE time + individually short SE scans

**→ DAX problem.**

Fusion is blocked, callbacks are present, or filters resolve iteratively. Fix the DAX.

See:

- `../patterns/_index.md` (Tier 1 DAX patterns)
- `../query-structure/_index.md` (Tier 2 query restructuring)

**Real example:** 109 SE queries, 30 % FE time → after restructuring: 4 SE queries, 1 % FE.

## Signal: Few SE queries + low FE time + high SE duration + low parallelism

**→ Data layout problem.**

The DAX is clean but SE scans are slow due to insufficient segments or poor compression. **DAX changes will not help.**

See:

- `../model-tuning/_index.md` (Tier 3 model patterns, especially General Data Layout Best Practices)
- `../model-tuning/dl001-v-ordering.md` and `dl002-segment-size.md` for Direct Lake

## Mixed signals

If both DAX and data layout problems exist, fix DAX first — Tier 1 patterns are non-destructive (auto-apply, semantic equivalence preserved). Then re-baseline; data layout issues become clearer once DAX noise is removed.

## Quick decision tree

```
Slow query
│
├─ Callbacks in trace? → Fix DAX (DAX002/007/008/018)
│
├─ Many SE queries, high FE % ? → Fix DAX (fusion patterns: DAX017/019/020)
│
├─ SE rows >> result rows ? → Fix DAX (push filters: DAX009/010)
│
├─ Few SE queries, low parallelism, clean xmSQL ? → Data layout (segments, V-order)
│
└─ Direct Lake + cold cache ? → DL001 (V-order) + DL002 (segment size)
```

## See also

- `architecture.md`
- `compression.md`
- `fusion.md`
- `trace-analysis.md` — full event waterfall
- `../decision-guide.md` — signal → specific pattern mapping
