# audit/ — atomic files

- `full-report.md` — one-shot audit via `pbir audit`
- `quick-checks.md` — fast smoke tests (page count, visual count per page)
- `pbir-validate.md` — interpreting `pbir validate` output: real errors vs CLI bundled-schema lag (false positives on report.json / pages.json / 2.9.0 visuals)
- `pbip-schema-drift.md` — `'$schema' is a required property` on a file you never touched: Desktop strips the key on every save. The `--fix-schema` repair and the hook that automates it
- `visual-design.md` — design-quality checklist (3-30-300, spacing, sorting)
- `layout-contract-validate.md` — conformance: did the build implement its approved `Design Brief:` (vs visual-design.md's generic quality)
- `performance.md` — query-time + render-time smell tests

## Order of operations

1. Start with `quick-checks.md` — kills 80% of issues in 10 seconds.
2. Run `full-report.md` for the structured audit.
3. Manually walk `visual-design.md` if the audience cares about design quality.
4. If the report was built from a `Design Brief:`, run `layout-contract-validate.md` to confirm the build matches the approved contract.
5. Run `performance.md` if the report feels slow or has > 12 visuals per page.
