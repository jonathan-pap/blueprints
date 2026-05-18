# SVG measure review checklist

Run after writing or modifying an SVG DAX measure, before showing to the user.

## Validation (pass / fail each)

1. **Data URI prefix** — Returned string starts with `"data:image/svg+xml;utf8,"`.
2. **xmlns** — `<svg>` element includes `xmlns='http://www.w3.org/2000/svg'`.
3. **viewBox** — Uses `viewBox` for responsive scaling (not fixed width / height alone).
4. **Color format** — Hex codes with `#` (e.g. `fill='#2196F3'`). No `%23` URL encoding, no named colors.
5. **Attribute quotes** — SVG attributes use single quotes to avoid DAX double-quote conflicts.
6. **DAX escaping** — Double quotes inside DAX strings escaped as `""`.
7. **HASONEVALUE guard** — Returns `BLANK()` when not in single-category context (for table / matrix measures).
8. **dataCategory** — Measure definition includes `dataCategory: ImageUrl` (in TMDL) or set via TOM.
9. **VAR structure** — SVG broken into VAR variables (Prefix, Content elements, Suffix). Aids readability and reuse.
10. **Coordinate system** — Y-axis inverted correctly (Y=0 at top in SVG).

## Design feedback (≤ 3 suggestions max)

- Complexity appropriate? (> 32K rendered chars will fail Power BI's image limit.)
- Coordinates rounded to 1–2 decimal places for render performance?
- Uses `CONCATENATEX` for series data (polyline / path)?
- Target visual type clear (table / matrix cell vs image vs card)?
- Colors muted and purposeful, not decorative?

## Verdict

`READY` (all 10 pass) — show to user.
`NEEDS CHANGES` (any fail) — list failures + fixes, do not show until corrected.

## Source / see also

- Pattern source: upstream `_examples/reports/agents/svg-reviewer.agent.md`
- Authoring guides: `../../02-build/visuals/svg/`
