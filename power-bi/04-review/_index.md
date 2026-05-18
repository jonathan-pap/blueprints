# 04-review — atomic file index

## audit/

- `full-report.md` — one-shot report audit via `pbir audit`
- `quick-checks.md` — fast smoke tests (page count, visual count per page)
- `visual-design.md` — design-quality checklist (3-30-300, spacing, sorting)
- `performance.md` — query-time + render-time smell tests

## bpa/

- `run.md` — execute BPA against the model
- `custom-rules.md` — add or customize BPA rules

## usage/

- `workspace.md` — Tier 1–3 workspace usage rollup
- `report-detail.md` — single report: daily views, viewer breakdown, page views
- `distribution.md` — who has access (direct, via role, via group)
- `exclude-non-consumers.md` — filter service principals, devs, IT from metrics

## structure/

- `validate-project.md` — full PBIP project validator (`validate_pbip.py`)
- `post-rename.md` — checklist after any cascade rename
- `utf8-bom-check.md` — detect and strip BOM-prefixed files

## export/

- `excel-for-qa.md` — export visual data tables to Excel for hand QA

## metadata/

- `file-summary.md` — sizes, modified times, dependencies between files

## reviewers/

- `_index.md` — picker
- `pbip-validator-checklist.md` — full PBIP project diagnostic flow
- `deneb-review.md` — Deneb spec review
- `svg-review.md` — SVG DAX measure review
- `python-review.md` — Python visual script review
- `r-review.md` — R visual script review

## Wired

- `hooks/README.md` — automated post-Write/Edit validation. Set up once per project.
- `scripts/` — executable Python and shell scripts the atomic files call.
- `usage-metrics-dataset/` — reference Power BI usage-metrics PBIP. Read-only.
