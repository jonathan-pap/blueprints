# lineage/ — atomic files

> Find downstream consumers of a semantic model — reports across the tenant, plus other consumer types you may have to check manually.

- `downstream-reports.md` — find Power BI reports bound to a model (no admin rights needed)
- `other-consumers.md` — what `downstream-reports.md` does NOT find (Excel, composite models, notebooks, etc.)
- `scripts/get-downstream-reports.py` — the underlying scanner

## When to use

- Before modifying or deleting a semantic model — impact analysis
- Auditing which reports are connected to a model
- Identifying orphaned or test reports against production models
- Cross-workspace dependency mapping

## Adjacent workflows

- After rename cascade in the model → run `downstream-reports.md` to find reports that need rebinding (`../../02-build/model/naming/downstream-impact.md`).
- For a full model audit → `../model-audit/_index.md`.
- For a focused report audit → `../audit/full-report.md`.
