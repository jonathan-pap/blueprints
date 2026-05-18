# dax/ — atomic files

> DAX performance optimization for semantic models. Tiered framework: Tier 1 (auto-apply patterns), Tier 2 (query structure — needs approval), Tier 3 (model changes — needs approval), Tier 4 (Direct Lake — needs approval).

## Workflow entry points

- `optimization-workflow.md` — phases 1–4: baseline → iterate → query structure → model changes
- `decision-guide.md` — trace signal → which pattern to start with

## Engine fundamentals (read once per session)

- `engine/architecture.md` — FE vs SE, query processing model
- `engine/xmsql.md` — Storage Engine query language seen in traces
- `engine/compression.md` — RLE, segments, parallelism, V-ordering
- `engine/fusion.md` — vertical + horizontal SE fusion, blockers
- `engine/trace-metrics.md` — FE/SE metrics derivation from `VertiPaqSEQueryEnd` events
- `engine/trace-analysis.md` — event types, what to look for, FE gap waterfall
- `engine/dax-vs-data-layout.md` — when DAX changes vs data layout changes apply

## Patterns (load only the ones matching the signal)

- `patterns/_index.md` — 21 Tier 1 DAX patterns (DAX001–DAX021); auto-apply
- `query-structure/_index.md` — 4 Tier 2 query patterns (QRY001–QRY004); user approval required
- `model-tuning/_index.md` — 10 Tier 3 model patterns (MDL001–MDL010) + 2 Tier 4 Direct Lake (DL001–DL002); user approval required

## Trace capture

- For local Power BI Desktop → `../../../03-bind/via-powershell/performance-profiling.md` and `evaluateandlog-debugging.md`
- For remote Fabric / XMLA → `powerbi-modeling-mcp` VS Code extension (`code --install-extension analysis-services.powerbi-modeling-mcp`)
- For workspace-wide history → Workspace Monitoring (Fabric)

## Related rooms

- For naming convention fixes (often surface during DAX work) → `../naming/`
- For Power Query / M expression optimization → `../power-query/`
- For full model audit including DAX anti-patterns → `../../../04-review/model-audit/`
- For per-measure live debugging via MCP → `../../../03-bind/via-mcp/query-dax.md` / `validate-dax.md`

## Source

Upstream `_examples/semantic-models/skills/dax/` (~67 KB across 4 references).
