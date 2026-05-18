# Audit workflow

Step-by-step procedure. Produces a prioritized markdown report.

## Step 0 — Gather context

**Critical.** Before any TMDL analysis, collect metadata + business context. See `gather-context.md`.

Run the metadata script:

```bash
python scripts/get_model_info.py -w <workspace-id> -m <model-id>
```

Returns: storage mode, model size, connected reports, deployment pipeline, endorsement status, sensitivity label, data sources, refresh schedule, last refresh, capacity SKU.

## Step 1 — Analyze model structure

Inspect TMDL via available tooling — use whatever's available to read tables, columns, measures, relationships, expressions. Common options:

- Tabular Editor (UI or CLI)
- `fab export` to TMDL on disk
- TMDL files directly if local (thick PBIP project)
- Programmatic access via XMLA / TOM (`../../03-bind/via-powershell/`)

## Step 2 — Run audit checks

Evaluate findings across categories — see `categories.md` for the full list. Categories ordered by severity:

1. **Critical** — bidirectional relationships, missing data types, orphaned tables, circular dependencies
2. **Memory and size** — high-cardinality columns, unsplit DateTime, auto date/time tables, attribute hierarchies, calc columns vs measures, unused columns
3. **Data reduction** — unfiltered history, pre-summarization opportunities, columns better handled upstream
4. **DAX anti-patterns** — filter-table-instead-of-column, missing DIVIDE, iterator+callback patterns, missing KEEPFILTERS
5. **Measure hygiene** — implicit measures used, report-scoped extension measures, duplicate measures
6. **Documentation** — missing descriptions, missing display folders, inconsistent naming
7. **Design** — star schema violations, missing/misconfigured date table, excessive columns per table, M2M without bridges, multiple fact tables without conformed dims
8. **Direct Lake (if applicable)** — Delta table health, DQ fallback risk
9. **AI readiness** — see `ai-readiness.md` for the dedicated checklist

## Step 3 — Performance analysis

For perf-specific work, see `performance.md`.

## Step 4 — Report findings

Output structure:

```markdown
# Semantic Model Audit Report

**Model:** [Name]
**Workspace:** [Name]
**Date:** YYYY-MM-DD

## Summary

| Severity        | Count |
|-----------------|-------|
| Critical        | X     |
| Performance     | X     |
| DAX Anti-Pattern| X     |
| Documentation   | X     |
| Design          | X     |

## Critical Issues

### [Issue Name]
- **Location:** [Table / Measure / Relationship]
- **Problem:** [Description]
- **Recommendation:** [Fix]

## Performance Issues
…

## Recommendations Priority

1. [Highest impact fix]
2. [Second priority]
…
```

Save to `../../outputs/$(date +%Y-%m-%d)-<model>-audit.md`.

## Caveats

- The structural audit analyzes metadata — it does NOT execute DAX queries or check data quality.
- For DAX query performance testing → `performance.md` + `../../02-build/model/dax/`.
- For companion report-level review → `../audit/full-report.md`.

## Dispatch the auditor agent

For a comprehensive audit handled autonomously: `../reviewers/semantic-model-auditor.md`. It performs the export, analysis, and reporting in one workflow.
