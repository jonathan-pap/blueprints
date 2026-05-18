# Decision guide — signal → pattern

Use to prioritize *where to start* within Tier 1 — not to skip patterns. Section 3 (Tier 1, DAX001–DAX021) is always read in full; these signals tell you which patterns to try first. Tier 2/3/4 signals are escalation triggers.

## Tier 1 — DAX patterns (auto-apply)

Pick the pattern matching the signal in the trace or measure code:

| Signal | Start with |
|---|---|
| `CallbackDataID` or `EncodeCallback` in xmSQL | DAX002, DAX007, DAX008, DAX018 (highest priority) |
| `ADDCOLUMNS` or `SUMMARIZE` in measure | DAX002, DAX006 |
| `SUMMARIZE` with complex / filtered table as first arg | DAX005 |
| `SUMX(VALUES(col), CALCULATE(...))` in measure | DAX006 |
| Same measure evaluated multiple times | DAX003 |
| Duplicate or redundant CALCULATE filters | DAX004 |
| `FILTER(Table, ...)` as CALCULATE arg, or `&&` joining predicates | DAX001 |
| `ALL(table), VALUES(table[col])` in same CALCULATE | DAX012 |
| Filter or `TREATAS` passed directly to `SUMMARIZECOLUMNS` (not wrapped in CALCULATETABLE) | DAX009 |
| SE rows far exceed final result count | DAX010 |
| `DISTINCTCOUNT` in measure | DAX011, DAX014 |
| Conditional logic (`IF`, `IIF`) or `DIVIDE()` inside iterator | DAX007, DAX018 |
| `SWITCH` or `IF` as primary expression body | DAX013 |
| Multiple SE queries hitting same fact table | DAX019 (vertical fusion), DAX020 (horizontal), DAX017 (boolean multiplier) |
| Near-identical SE queries differing only by filter value or per-measure `VAND` tuple predicates on same column | DAX017 |
| Bidirectional or M2M causing unexpected SE join expansion; or existing `TREATAS`/`CROSSFILTER` in measure | DAX016 |
| High-cardinality iterator + low-card attribute | DAX015 |
| `TREATAS`/`IN` re-filtering same fact with computed key set; large compound-tuple semi-join in xmSQL | DAX021 |

**No signal matches?** Read all of `patterns/_index.md` — patterns DAX001–DAX021 cover the full range.

## Tier 2 — Query structure (escalation)

Only consult when corresponding signal is present. All require **user approval**.

| Signal | Escalate to |
|---|---|
| `__ValueFilterDM` in generated query | QRY002 |
| Groupby column high-cardinality (e.g., `Calendar[Date]`) | QRY003 |
| Tier 1 exhausted; output change acceptable | QRY001–QRY004 |

## Tier 3 — Model patterns (escalation)

| Signal | Escalate to |
|---|---|
| Few SE queries + low parallelism + clean xmSQL + high SE duration | Data layout (MDL001–MDL010) |
| Many-to-many or bidirectional overhead | MDL001 |
| Bidir for security/dim mix; consistent vs peak perf trade-off | MDL001 sub-pattern matrix |
| High-cardinality columns dominating model size | MDL003 |
| TI scans for fixed period comparisons (YoY, MoM) on large DQ | MDL005 |
| TI breaks vertical fusion across many period measures | MDL006 |
| Slow SWITCH/multi-measure with `__ValueFilterDM` traces | MDL007 (RI violations) |
| `SEARCH()`/`FIND()` filter forcing row-by-row scan | MDL008 |
| Disconnected slicer triggering 2 evaluation branches when no selection | MDL010 |

## Tier 4 — Direct Lake (escalation)

| Signal | Escalate to |
|---|---|
| Direct Lake + low parallelism or cold cache | DL001 (V-ordering) |
| Direct Lake + few segments (table > 1M rows in < 4 segments) | DL002 (segment size) |

## Workflow order

1. Apply Tier 1 patterns matching signals above (auto, iterate).
2. If Tier 1 exhausted and < 10 % improvement → escalate to Tier 2 with user approval.
3. If Tier 2 not applicable or output change unacceptable → Tier 3.
4. If Direct Lake-specific → Tier 4.

See `optimization-workflow.md` for the full phased process.
