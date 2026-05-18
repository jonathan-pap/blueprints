# Optimization workflow (4 phases)

End-to-end DAX optimization. Always read this before starting any optimization session.

## Tiers and autonomy

| Tier | Scope | Autonomy |
|---|---|---|
| **Tier 1 — DAX patterns** | Rewrite measure/UDF definitions | **Auto-apply.** Keep EVALUATE/grouping identical. |
| **Tier 2 — Query structure** | Modify EVALUATE, grain, filters | **User approval required.** Present recommendation first. |
| **Tier 3 — Model changes** | Relationships, columns, agg tables, data types | **High caution.** Discuss trade-offs. Suggest model copy. Warn downstream risk. |
| **Tier 4 — Direct Lake** | OneLake layout, V-ordering, rowgroup sizing | **High caution.** Requires ETL / pipeline changes outside the model. |

**Success criteria — Tier 1:** ≥ 10 % duration improvement AND semantic equivalence (same row count, columns, values).
**Tier 2/3/4:** ≥ 10 % improvement AND explicit user approval of structural or output changes.

## Requirements

- **Semantic model connection** — local Desktop via `../../../03-bind/via-powershell/quickstart.md`; remote via `powerbi-modeling-mcp` or equivalent XMLA-capable tool.
- **Trace capture** — server timing trace required. See `engine/trace-metrics.md`.
- **Model metadata** — ability to read measure / function / calc group definitions, table metadata, relationships.

## Phase 1 — Establish baseline

### Step 1 — Resolve all measure and function definitions

Before optimizing, fully resolve every DAX expression in the query. Partial visibility = incorrect optimizations.

1. Identify measure references in the user's query (any `[MeasureName]`).
2. Retrieve each measure's definition (name, table, DAX).
3. Recursively resolve dependencies (nested `[OtherMeasure]` calls).
4. Retrieve user-defined functions if referenced.
5. Build a DEFINE block inlining all resolved measures and functions.
6. Check for active calculation groups — list all, retrieve calculation item expressions.

Example:

```dax
DEFINE
    MEASURE 'Sales'[Total Revenue] = SUM('Sales'[Revenue])
    MEASURE 'Sales'[Total Profit]  = SUM('Sales'[Revenue]) - SUM('Sales'[Cost])
    MEASURE 'Sales'[Profit Margin] = DIVIDE([Total Profit], [Total Revenue])

EVALUATE
SUMMARIZECOLUMNS('Product'[Category], "Profit Margin", [Profit Margin])
```

### Step 2 — Gather model context

1. List all tables — storage modes (Import / DQ / Direct Lake).
2. List all relationships — join paths, filter propagation.

Distinguishes model design issues from DAX expression problems.

### Step 3 — Execute baseline (1 warm-up + 3 measured)

For each run:

1. Clear VertiPaq cache (cold-cache timing).
2. Execute with server timing trace enabled.
3. Derive: Total Duration, FE/SE split, SE query count, peak memory, result row count. See `engine/trace-metrics.md` for derivation.
4. Record full metrics, trace events, baseline result data (for semantic equivalence later).

After all runs: discard warm-up, take **median** of 3 as baseline. If results spread > 20 %, run 5 more iterations to isolate platform noise.

**Isolating measures:** When trace is noisy with many measures, comment out all but one (or small group), re-run, compare. Repeat to identify which drive total duration.

### Step 4 — Analyze baseline

Apply `engine/trace-analysis.md` to interpret. Use `decision-guide.md` to identify which Tier 1 patterns to try first.

## Phase 2 — Optimization iterations

### Step 1 — Select and apply (Tier 1)

Identify DAX patterns present in baseline measures. Apply DAX001–DAX021 from `patterns/`.

**CRITICAL:** Modify only **measure definitions in DEFINE block**. Do NOT change EVALUATE clause or grouping columns — query structure must stay identical to preserve semantic equivalence.

### Step 2 — Execute and compare

1. Clear cache.
2. Execute with trace.

**During iteration:** 1 run sufficient (columns already resident from baseline). Reserve full protocol (1 warm-up + 3 measured, median) for **final confirmation** vs original baseline.

**Evaluate:**

- Improvement = (BaselineDuration − OptimizedDuration) / BaselineDuration × 100
- Semantic equivalence: compare CSV result vs baseline CSV — same rows, columns, values. If different → optimization changed semantics → revert. Check **immediately** after each iteration.

### Step 3 — Iterate and escalate

- **≥ 10 % improvement + semantically equivalent** → success. Present + offer as new baseline (compound improvements common).
- **Further rounds:** re-run Phase 1 Steps 3–4 on new baseline. Different structure → re-analyze against decision guide.
- **< 10 % improvement** → try another Tier 1 pattern. Re-examine trace for additional bottlenecks.
- **Results differ** → revert. Optimization changed semantics.
- **Tier 1 exhausted** → Phase 3 (Tier 2) with user approval.

## Phase 3 — Query structure (Tier 2)

> **STOP — explicit user approval required.**

Consult `query-structure/_index.md` (QRY001–QRY004).

Before applying:

1. Explain the specific change ("Group by YearMonth instead of Date reduces result rows from 365K to 12K").
2. Explain what changes in output and what perf user gains.
3. Wait for explicit approval.
4. If approved, modify, run full baseline cycle, present results.

## Phase 4 — Model and data layout (Tier 3/4)

> **STOP — explicit user approval required.**

Consult `model-tuning/_index.md` (MDL001–MDL010, DL001–DL002).

Before proceeding:

1. Present specific diagnosis and proposed model change.
2. Explain why current design causes the bottleneck.
3. **Warn that model changes can break downstream reports.** Run `../../../04-review/lineage/downstream-reports.md` to assess impact.
4. Suggest a model copy for experimentation.
5. Identify if upstream changes (Lakehouse, Warehouse, Power Query) are required — those can't be done through model tooling alone.
6. If approved, coordinate with CI/CD.
7. After applying, re-run the full baseline optimization workflow to measure impact.

## Error handling

- **Connection failure** — verify dataset/workspace name or XMLA endpoint. Local Desktop running? Service XMLA read/write enabled?
- **Query syntax error** — validate DAX before executing.
- **Semantic equivalence failure** — review filter context, aggregation granularity, CALCULATE filter args. Revert and try differently.
- **No improvement found** — query may already be well-optimized at DAX level. Check Phase 3 / 4.
- **Trace events empty** — server timing / trace capture enabled? Subscribed to `QueryEnd`, `VertiPaqSEQueryEnd`, `VertiPaqSEQueryCacheMatch`?
