# naming/ — atomic files

> Interactive workflow for standardizing TMDL names — tables, columns, measures, display folders.

## Foundation

- `core-principle.md` — names must reflect business terminology, not technical conventions
- `audit-workflow.md` — phased process: discover → context → audit → apply → validate
- `naming-rules.md` — the 11 rule categories (no programming case, no abbreviations, no tech prefixes, consistent aggregation/unit/period syntax, etc.)
- `measure-name-construction.md` — the canonical order `[Aggregation] [Base Name] [Period] ([Unit])`
- `downstream-impact.md` — warning: renames break visual bindings; rebind cascade procedure

## When to enter

User asks: "standardize naming", "fix naming conventions", "clean up model names", "audit naming", "make names human-readable", or mentions renaming for consistency.

## Cross-references

- After renaming model objects → run `../../report/pbip-format/rename-measure.md` / `rename-column.md` / `rename-table.md` for the report-side cascade.
- For the auditor agent that flags naming issues → `../../../04-review/reviewers/semantic-model-auditor.md`.
- Source: upstream `_examples/semantic-models/skills/standardize-naming-conventions/`.
