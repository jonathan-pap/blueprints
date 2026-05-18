# Python visual review checklist

Run after writing or modifying a Python visual script, before showing to the user.

## Validation (pass / fail each)

1. **`plt.show()` present** — Must be the final line. Nothing renders without it.
2. **`dataset` not created** — The DataFrame is auto-injected by Power BI. Script must not define it.
3. **Column names** — Match `nativeQueryRef` display names from field bindings exactly.
4. **Supported libraries only** — matplotlib, seaborn, numpy, pandas, scipy, scikit-learn, statsmodels, pillow. **No plotly, bokeh, altair.**
5. **No networking** — Zero URL fetches, API calls, or file downloads.
6. **Single plot** — Only the last `plt.show()` renders. Multiple figures not supported.
7. **Empty-data guard** — Handles `dataset.empty` gracefully (no traceback).
8. **figsize set** — `plt.subplots(figsize=(w, h))` for proper aspect ratio at 72 DPI.

## Design feedback (≤ 3 suggestions max)

- Prefer seaborn over raw matplotlib for cleaner defaults?
- Chart chrome minimal (remove top / right spines)?
- Colors hex-coded and muted (not matplotlib defaults)?
- Text sizes readable at 72 DPI output?
- `tight_layout()` called to prevent clipping?

## Verdict

`READY` (all 8 pass) — show to user.
`NEEDS CHANGES` (any fail) — list failures + fixes, do not show until corrected.

## Source / see also

- Pattern source: upstream `_examples/reports/agents/python-reviewer.agent.md`
- Authoring guides: `../../02-build/visuals/python/`
