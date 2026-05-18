# Deneb visual review checklist

Run after writing or modifying a Deneb Vega / Vega-Lite spec, before showing to the user.

## Validation (pass / fail each)

1. **Schema** — `$schema` points to a valid Vega or Vega-Lite schema URL.
2. **Data binding** — Vega uses `"data": [{"name": "dataset"}]` (array); Vega-Lite uses `"data": {"name": "dataset"}` (object).
3. **Field names** — Match `nativeQueryRef` display names from the visual's bindings. Special chars (`.[]"`) become `_`; spaces preserved.
4. **Expression escaping** — Field refs with spaces use double quotes: `datum["Field Name"]`. Never single quotes.
5. **Responsive sizing (Vega only)** — Uses `pbiContainerWidth` / `pbiContainerHeight` signals.
6. **Config block** — Includes `autosize: "fit"`, `view.stroke: "transparent"`, `font: "Segoe UI"`.
7. **Theme colors** — Uses `pbiColor()` / `pbiColorNominal` rather than hardcoded hex where possible.
8. **Marks** — Encode blocks use `enter` / `update` / `hover` (Vega) or proper encoding channels (Vega-Lite).
9. **Tooltips enabled** — `"tooltip": {"signal": "datum"}` or `"tooltip": true`.
10. **No external data** — Zero URL-based data sources (blocked by AppSource certification).

## Design feedback (≤ 3 suggestions max)

- Chart type appropriate for the relationship being shown?
- Color use intentional (not decorative)?
- Axes / legends minimal and readable?
- Text sizes ≥ 12pt for labels?
- Sort order sensible (value descending unless time-based)?

## Verdict

`READY` (all 10 pass) — show to user.
`NEEDS CHANGES` (any fail) — list failures + fixes, do not show until corrected.

## Source / see also

- Pattern source: upstream `_examples/reports/agents/deneb-reviewer.agent.md`
- Authoring guides: `../../02-build/visuals/deneb/`
