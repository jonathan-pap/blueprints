# Performance audit

When a report feels slow, or proactively before release.

## Quick smell tests

```bash
# Visual count per page (more than ~12 = potential perf issue)
for d in "<project>.Report/definition/pages/"*/; do
  echo "$(basename "$d"): $(ls "$d/visuals/" 2>/dev/null | wc -l)"
done

# Custom visuals (often slow to render)
grep -rE '"visualType":"(?!(card|cardVisual|kpi|line|bar|column|table|matrix|slicer|textbox|image|shape|filter))' \
  "<project>.Report/definition/pages/"

# DAX queries embedded in visuals
find "<project>.Report" -name "*.dax" | wc -l
```

## Python script for full perf audit

```bash
python scripts/performance_audit.py "<project>.Report" \
  -o ../../outputs/$(date +%Y-%m-%d)-<project>-perf.log
```

Returns:
- Refresh history timings (if connected to the published model)
- Long-running queries
- Visuals with highest query cost
- Suggestions per finding

## Live profiling

For per-visual query timings, capture queries from the live model:

- `../../03-bind/via-powershell/query-listener.md` — TOM trace
- `../../03-bind/via-powershell/performance-profiling.md` — server timings, query plan

## Common fixes

- **Too many visuals** → split into pages or remove low-value charts.
- **Custom visuals everywhere** → replace with native where possible.
- **Big tables (`tableEx`, `pivotTable`) with no filters** → add page filters.
- **Calc columns recomputed often** → consider moving to a precomputed column at source.
- **Heavy DAX in measures** → see `../../03-bind/via-powershell/evaluateandlog-debugging.md`.
