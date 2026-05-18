# Model performance analysis

Memory, query, and unused-column analysis. For DAX query-level optimization see `../../02-build/model/dax/`.

## Tooling

- **Tabular Editor 3 — VertiPaq Analyzer** — per-column memory footprint, dictionary sizes, encoding types, cardinality. First step for any memory investigation.
- **Tabular Editor 3 — Best Practice Analyzer** — rule-based structural checks
- **DAX Studio** — server timings, VertiPaq scan statistics, query plans, xmSQL. Diagnosing slow individual DAX queries.
- **Performance Analyzer (Power BI Desktop)** — per-visual query timing in report context
- **Workspace Monitoring (Fabric)** — historical query logs in KQL database for ongoing prod monitoring

## Workflow

1. Run **VertiPaq Analyzer** to identify memory hotspots (large dictionaries, high-cardinality columns)
2. Run **Best Practice Analyzer** with an appropriate ruleset (`../bpa/`)
3. Use **DAX Studio** to test specific slow queries with server timings (or `../../02-build/model/dax/optimization-workflow.md` for systematic optimization)
4. Use **Performance Analyzer** in Desktop to identify which report visuals generate expensive queries
5. For prod monitoring: enable **Workspace Monitoring** + deploy dashboards from microsoft/fabric-toolbox

## Memory and size

### What to look for

- **Total model size** vs capacity SKU
- **Column cardinality** — GUIDs, transaction IDs, composite keys inflate dictionaries
- **DateTime columns** — split into Date + Time (90%+ memory reduction)
- **Text column avg length** — long values inflate dictionaries
- **Unused columns** — columns not referenced by any measure, relationship, or visual

### Unused column detection

| Approach | How | Caveats |
|---|---|---|
| TMDL grep (static) | grep all `.tmdl` for column refs in measures, calc columns, relationships | Misses references from report visual bindings |
| Workspace Monitoring (runtime) | Query logs reveal which columns are actually scanned | Need sustained log period |
| SemanticModelAudit (automated) | Notebook in microsoft/fabric-toolbox compares Delta schemas with model columns | Direct Lake only |

### Common optimizations

- Remove / hide unnecessary columns (especially GUIDs, composite keys, transaction IDs)
- Split DateTime → Date + Time
- Disable Auto Date/Time tables
- Disable attribute hierarchies (`IsAvailableInMDX = false`) on hidden / high-card columns
- Move calc columns → Power Query computed columns where possible
- Reduce text precision (trim, truncate long descriptions)
- Appropriate data types (Integer vs Double for whole numbers)

## DAX query performance

### Cache states

Always specify which state was measured. Test results vary 10–100× across states.

| State | Meaning | How to achieve |
|---|---|---|
| **Cold** | No data in memory; load from disk | Pause/resume capacity (Import); clearValues refresh (Direct Lake) |
| **Warm** | Data framed in memory but VertiPaq cache cleared | Priming query + `CALL [ClearCache]` in DAX Studio |
| **Hot** | Data + VertiPaq cache both populated | Run query twice; second is hot |

**Test with warm or hot for typical user experience.** Cold is worst-case (first user after refresh / capacity resume).

### Methodology

1. Run each query 3+ times per cache state (ideally 10+)
2. Measure in Power BI service, not locally (local doesn't reflect production capacity)
3. Use DAX Studio server timings to separate SE from FE time
4. A single test misleads — always use multiple iterations
5. Compare before / after under controlled conditions

### Common DAX perf issues (high-level)

| Pattern | Why slow | Fix |
|---|---|---|
| Nested CALCULATE with complex filters | Multiple context transitions | Simplify; use variables |
| SUMX / AVERAGEX over large unfiltered tables | Row-by-row evaluation | Add filters; pre-aggregate |
| Division without DIVIDE() | Error propagation | `DIVIDE(num, den, 0)` |
| ALL() instead of REMOVEFILTERS() | Semantic ambiguity | REMOVEFILTERS() for explicit removal |
| Calc columns with complex DAX | Evaluated for every row during refresh | Move to Power Query; use measures |
| High-cardinality DISTINCTCOUNT | Full dictionary scan | Approximate DISTINCTCOUNT or pre-aggregation |

Full pattern catalog → `../../02-build/model/dax/patterns/_index.md`.

## Benchmarking + AI-assisted optimization

- [DAXPerformanceTesting notebook](https://github.com/microsoft/fabric-toolbox/tree/main/tools/DAXPerformanceTesting) — automates cache clearing, capacity management, trace capture
- [DAXPerformanceTunerMCPServer](https://github.com/microsoft/fabric-toolbox/tree/main/tools/DAXPerformanceTunerMCPServer) — anti-pattern detection + optimization suggestions with semantic equivalence checking

## Performance targets

No universal targets. Always consider the consumer's perspective. **Generally aim for sub-second queries for visuals.** Document targets and communicate to model developers; consider as prerequisites for endorsement (certified models).
