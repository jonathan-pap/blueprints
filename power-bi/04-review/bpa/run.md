# Run Best Practice Analyzer (BPA)

BPA scans the semantic model against a ruleset (data quality, performance, naming).

## Via pbir

```bash
pbir bpa run "<project>.SemanticModel" \
  -o ../../outputs/$(date +%Y-%m-%d)-<project>-bpa.md
```

Uses the default ruleset (Microsoft's curated rules).

## Use a custom ruleset

```bash
pbir bpa run "<project>.SemanticModel" \
  --rules path/to/MyRules.json \
  -o ../../outputs/$(date +%Y-%m-%d)-<project>-bpa.md
```

See `custom-rules.md` to author your own.

## Read the output

Severity:
- **Error** — broken or anti-pattern (e.g. unused column, missing format string).
- **Warning** — performance / hygiene suggestion.
- **Info** — style / convention notes.

For each finding the report lists: object name, rule violated, suggested fix.

## Common findings

- `[Performance] Column too large` — calc column would be cheaper as physical column.
- `[Naming] Table name contains spaces` — fine for display but adds quoting noise everywhere.
- `[Data quality] No description on measure` — add `///` line (see `../../02-build/model/fix-pattern/missing-description.md`).
- `[Hygiene] Visible column not used in any visual or measure` — candidate for `isHidden`.

## Custom ruleset shipping

Keep `BPARules.json` next to the project in `projects/<name>/`. Reference from BPA runs. Don't bundle here in the blueprint — rules tend to be project-specific.
