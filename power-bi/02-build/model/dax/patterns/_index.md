# patterns/ — Tier 1 DAX optimization patterns

> **Auto-apply freely.** Modify only measure/UDF definitions in the DEFINE block. Keep EVALUATE and SUMMARIZECOLUMNS grouping identical to preserve semantic equivalence.

> **Prefer SUMMARIZECOLUMNS:** Fully supported inside measure definitions — earlier restrictions no longer apply. Use it to replace `ADDCOLUMNS`/`SUMMARIZE` patterns (DAX002), pre-materialize context transitions before iterating (DAX006), and cache repeated evaluations into a single virtual table (DAX003). Prefer over `ADDCOLUMNS(VALUES(...), ...)` unless a specific scenario prevents it.

## Patterns

- `dax001-simple-column-filters.md` — column predicates as CALCULATE args, not FILTER tables
- `dax002-summarizecolumns.md` — replace ADDCOLUMNS / SUMMARIZE with SUMMARIZECOLUMNS
- `dax003-cache-in-variables.md` — cache repeated and context-independent expressions
- `dax004-remove-duplicate-filters.md` — remove redundant CALCULATE filters and predicates
- `dax005-summarize-complex-table.md` — wrap with CALCULATETABLE instead of SUMMARIZE complex table
- `dax006-pre-materialize-context-transition.md` — materialize context transitions with SUMMARIZECOLUMNS
- `dax007-replace-if-with-int.md` — INT for boolean conversion avoids callback
- `dax008-context-transition-in-iterator.md` — three ways to fix expensive context transitions
- `dax009-wrap-summarizecolumns-filters.md` — move filters to wrapping CALCULATETABLE
- `dax010-calculatetable-not-filter.md` — apply filters with CALCULATETABLE instead of FILTER
- `dax011-distinct-count-alternatives.md` — SUMX(VALUES(), 1) when FE-bound is faster
- `dax012-allexcept-instead-of-all-values.md` — single ALLEXCEPT vs ALL+VALUES restoration
- `dax013-switch-if-branch-optimization.md` — SUMMARIZECOLUMNS branch optimization gotchas
- `dax014-countrows-not-distinctcount.md` — COUNTROWS on key columns instead of DISTINCTCOUNT
- `dax015-lower-granularity-iterator.md` — iterate the low-card attribute, not the high-card table
- `dax016-treatas-crossfilter-override.md` — experiment with relationship overrides
- `dax017-boolean-multiplier.md` — boolean multiplier to unblock horizontal fusion
- `dax018-divide-vs-slash-in-iterators.md` — `/` instead of DIVIDE() inside iterators
- `dax019-vertical-fusion-ti.md` — lift time intelligence to outer CALCULATE
- `dax020-horizontal-fusion.md` — keep base measures TI-free
- `dax021-precompute-and-join.md` — NATURALINNERJOIN instead of TREATAS round-trip

## How to choose

Use `../decision-guide.md` to map a trace signal to a starting pattern. If no signal matches, scan all 21 and apply the ones that fit your measure code.

## After applying

Per `../optimization-workflow.md` Phase 2 Step 2:

- ≥ 10 % improvement + semantic equivalence → success, offer as new baseline
- < 10 % → try another pattern
- Results differ → revert, optimization changed semantics
