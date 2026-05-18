# Room 04 — Review

> Validate, audit, and assess. Structural validation is automated via `hooks/`. Design / usage review is scripted but manual.

## Three review scenarios

- **Under development** → focus on structure, BPA, performance smell-tests.
- **In testing** → add deployed-report metadata, early user feedback.
- **In use** → **usage and adoption is the primary signal**. A beautiful unused report is a maintenance liability.

## Workflow router

- **Validate after every edit** → already wired via `hooks/` (set up once per project).
- **Run a full PBIP audit** → `audit/_index.md`
- **Run BPA rules against the model** → `bpa/run.md`
- **Performance smell tests / timings** → `audit/performance.md`
- **Workspace-wide usage rollup** → `usage/workspace.md`
- **Single-report deep dive** → `usage/report-detail.md`
- **Who has access** → `usage/distribution.md`
- **Filter out non-consumers from usage** → `usage/exclude-non-consumers.md`
- **PBIP project structural check** → `structure/validate-project.md`
- **After a cascade rename** → `structure/post-rename.md`
- **Check for UTF-8 BOM** → `structure/utf8-bom-check.md`
- **Export visual data to Excel for QA** → `export/excel-for-qa.md`
- **Read file size / dependencies / modified time** → `metadata/file-summary.md`
- **Review a Deneb / SVG / Python / R visual before showing the user** → `reviewers/_index.md`
- **Full PBIP diagnostic flow** → `reviewers/pbip-validator-checklist.md`

## Outputs go to outputs/

Every artifact this room produces lands in `../outputs/` with `YYYY-MM-DD-<project>-<type>.<ext>` naming.

Common types:

- `audit` (`.md`)
- `bpa` (`.md` / `.json`)
- `perf` (`.log` / `.json`)
- `usage` (`.json`)
- `distribution` (`.csv`)

## What's here

- `_index.md` — full atomic-file picker
- `audit/`, `bpa/`, `usage/`, `structure/`, `export/`, `metadata/`, `reviewers/` — atomic workflow steps
- `hooks/` — opt-in validation hooks (with their own README)
- `scripts/` — Python audit and usage scripts
- `usage-metrics-dataset/` — reference Power BI usage-metrics PBIP for understanding the schema
