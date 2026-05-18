# MDL004 — Aggregation table strategies

> Tier 3 — user approval required. Requires DirectQuery or composite model setup.

Pre-summarized Import tables intercept SE queries before they hit large DirectQuery facts. Aggregate Awareness redirects automatically — no DAX changes.

## Setup

1. Build the aggregation: `GROUP BY [FKs], SUM([Metrics])` on the source.
2. Load as **Import** mode.
3. Connect to the same dimensions as the detail fact.
4. Map in Power BI Desktop → Manage Aggregations:
   - For each metric in the agg table: `SUM OF [DetailFact[Column]]`.

Fact tables (the underlying detail) must be DirectQuery for the redirection to fire.

## Filtered aggs (hot/cold split)

Import only recent data — e.g., last 3 months. Older queries fall through to DirectQuery.

**Result:** 95 %+ of queries served from the small import aggregation. Only deep historical queries hit the slow DQ path.

## When to use

- Detail fact is too large for full import (> 100 M rows, > 10 GB)
- Queries are predictable — most ask for last 30/90 days at aggregated grain
- DirectQuery latency is acceptable for the rare deep query

## When NOT to use

- All queries are detail-level (no aggregation possible)
- Aggregation grain doesn't match common query patterns (Aggregate Awareness won't fire)
- Detail fact already fits in memory (Import the whole thing)

## Verify it's working

The trace event `AggregateTableRewriteQuery` fires when the engine successfully redirects a query to the agg table. If it's missing on an agg-enabled query, the redirection failed (check column mappings and query grain).
