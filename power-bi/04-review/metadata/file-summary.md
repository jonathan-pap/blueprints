# File-level metadata summary

Sizes, modified times, dependencies — useful for "is this report still being touched", "what does the project actually look like on disk".

## Sizes per top-level area

```bash
PROJ="<project>"
du -sh "$PROJ.Report" "$PROJ.SemanticModel" 2>/dev/null
```

## File count per type

```bash
find "$PROJ" -name "*.tmdl" | wc -l   # TMDL files
find "$PROJ" -name "*.json" | wc -l   # JSON files (PBIR + others)
find "$PROJ" -name "*.dax"  | wc -l   # saved DAX queries
```

## Largest files (often the trouble)

```bash
find "$PROJ" -type f -exec wc -c {} \; | sort -rn | head -10
```

Common offenders:
- Theme JSONs (often 75 KB+ if not serialized).
- Visual JSONs with bespoke overrides (10 KB+ is a smell — see `../audit/full-report.md`).
- DAX query files with stale query text.

## Last-modified across the project

```bash
find "$PROJ" -type f -name "*.tmdl" -o -name "*.json" | \
  xargs ls -la --time-style=long-iso | sort -k 6,7 | tail -20
```

Shows the most recently-touched files. Useful before a code review.

## Dependency map (cross-references)

```bash
# Every visual.json's bound fields → which model objects they reference
pbir fields list "$PROJ.Report" -F json
```

Or grep for model object names across the report:

```bash
grep -rl "'Sales'" "$PROJ.Report/"   # everything referencing the Sales table
```

## Output

Drop a summary file in `../../outputs/`:

```bash
echo "..." > ../../outputs/$(date +%Y-%m-%d)-<project>-file-summary.md
```
