# audit/ — atomic files

- `full-report.md` — one-shot audit via `pbir audit`
- `quick-checks.md` — fast smoke tests (page count, visual count per page)
- `visual-design.md` — design-quality checklist (3-30-300, spacing, sorting)
- `performance.md` — query-time + render-time smell tests

## Order of operations

1. Start with `quick-checks.md` — kills 80% of issues in 10 seconds.
2. Run `full-report.md` for the structured audit.
3. Manually walk `visual-design.md` if the audience cares about design quality.
4. Run `performance.md` if the report feels slow or has > 12 visuals per page.
