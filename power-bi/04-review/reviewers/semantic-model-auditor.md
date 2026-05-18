# Semantic model auditor — checklist

Comprehensive model audit. Run when the user asks: "audit a semantic model", "check for performance issues", "run a best practice audit", or "audit the model against best practices before we go to production".

## Workflow

### Step 1 — Export the model (if remote)

```bash
fab export "Workspace.Workspace/Model.SemanticModel" -o /tmp/audit -f
```

For thick PBIP projects on disk, skip this — TMDL is already there at `<project>.SemanticModel/definition/`.

### Step 2 — Analyze TMDL structure

```
<model>.SemanticModel/
├── definition/
│   ├── model.tmdl          # Model-level settings
│   ├── database.tmdl       # Database config
│   ├── tables/             # Table definitions
│   ├── relationships.tmdl  # Relationships
│   └── expressions.tmdl    # M expressions
```

### Step 3 — Run audit checks

Use the full check catalog from `../model-audit/categories.md`. Below is the agent's quick PASS/FAIL/INFO summary per category:

## Critical (4)

- **Bidirectional relationships** — `crossFilteringBehavior: bothDirections` in `relationships.tmdl`. Recommend single-direction unless explicitly required.
- **Missing data types** — all columns must have explicit `dataType:`.
- **Circular dependencies** — parse measure definitions, build dep graph, flag cycles.
- **Orphaned tables** — no relationships to anything.

## Memory and size (8)

- **High-cardinality columns** — GUIDs, transaction IDs, composite keys, near-unique strings. Recommend removing if unused, splitting if needed.
- **Unsplit DateTime columns** — second/millisecond precision. Split into Date + Time (90 %+ reduction).
- **Auto Date/Time tables** — hidden `LocalDateTable_*` / `DateTableTemplate_*`. Disable Auto Date/Time in Desktop.
- **`IsAvailableInMDX` on hidden / high-card columns** — wastes memory on unused attribute hierarchies. Set to false.
- **Inappropriate data types** — Double for currency (use Fixed Decimal / Currency.Type); String for numeric.
- **Calculated columns that could be measures** — count `expression:` in column blocks; flag aggregations.
- **Unused columns** — cross-reference column names against measure DAX, relationships, hierarchies. If report is available, against visual bindings.
- **DISTINCTCOUNT on high cardinality** — find measures using DISTINCTCOUNT, flag if target column has high cardinality. Alternative: see DAX011 in `../../02-build/model/dax/patterns/`.

## DAX anti-patterns (4 — flag presence, optimize via `../../02-build/model/dax/`)

- **Nested CALCULATE** — regex `CALCULATE\s*\([^)]*CALCULATE`.
- **Division without DIVIDE / IFERROR** — find `/` in measures.
- **Iterators over large unfiltered tables** — SUMX, AVERAGEX without FILTER context.
- **ALL() instead of REMOVEFILTERS()** — find `ALL(TableName)` in CALCULATE filter args.

## Documentation (3)

- **Missing descriptions** — count tables/columns/measures lacking `///` lines.
- **Missing display folders** — count measures without `displayFolder:`.
- **Inconsistent naming** — see `../../02-build/model/naming/` for rules.

## Design (4)

- **Star schema violations** — flag dim tables with outgoing relationships (snowflake); flag fact-to-fact relationships.
- **Excessive columns per table** — >100 = unwieldy; >30 = denormalization smell.
- **Missing date table** — look for `dataCategory: Time`; missing breaks time intelligence.
- **Data reduction issues** — unfiltered history in fact tables; calc columns better moved to Power Query.

## Direct Lake (2 — if applicable)

- **Parquet file count** — > 10 000 = framing fail. Note model is DL and recommend Delta health check (`OPTIMIZE`, `VACUUM`).
- **DirectQuery fallback risk** — RLS definitions in `roles.tmdl`; views referenced. Note DQ fallback degrades perf.

## AI readiness (2 — see `../model-audit/ai-readiness.md` for full)

- **Duplicate field names across tables** — `Name` in both Customer and Store confuses Copilot.
- **Model complexity for AI** — flag disconnected tables, M2M without bridge, inactive relationships. Not "bad practices" but harder for AI.

## Output

Structured markdown report in `../../outputs/$(date +%Y-%m-%d)-<model>-audit.md`:

```markdown
# Semantic Model Audit Report

**Model:** [Name] **Workspace:** [Name] **Date:** YYYY-MM-DD

## Summary
| Severity | Count |
|---|---|

## Critical Issues
### [Issue Name]
- **Location:** [Table/Measure/Relationship]
- **Problem:** [Description]
- **Recommendation:** [Fix]

## Performance Issues
…

## Recommendations Priority
1. [Highest impact fix]
2. [Second priority]
```

## Additional API checks (deployed models)

```bash
# Refresh history
WS_ID=$(fab get "Workspace.Workspace" -q "id" | tr -d '"')
MODEL_ID=$(fab get "Workspace.Workspace/Model.SemanticModel" -q "id" | tr -d '"')
fab api -A powerbi "groups/$WS_ID/datasets/$MODEL_ID/refreshes?\$top=5"

# Model info
fab api -A powerbi "groups/$WS_ID/datasets/$MODEL_ID"
```

Or use `../model-audit/scripts/get_model_info.py` for the structured version.

## Verdict

`READY` (no Critical, ≤ 3 high-priority recommendations) — show user.
`NEEDS CHANGES` (Critical issues or >3 high-priority) — list + fixes; recommend addressing before promoting to prod.

## Source

Pattern source: upstream `_examples/semantic-models/agents/semantic-model-auditor.agent.md`.
Full check catalog: `../model-audit/categories.md`.
AI readiness sub-checklist: `../model-audit/ai-readiness.md`.
