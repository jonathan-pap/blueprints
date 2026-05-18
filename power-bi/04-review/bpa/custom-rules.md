# Author / customize BPA rules

Rules live in a JSON file. Microsoft's default set is a good starting point; copy and modify.

## Get the default set

```bash
pbir bpa rules --export -o ./BPARules.json
```

## Rule shape

```json
{
  "ID": "MyRule",
  "Name": "All measures should have a format string",
  "Category": "Maintenance",
  "Severity": 2,
  "Scope": "Measure",
  "Expression": "string.IsNullOrEmpty(FormatString)",
  "Description": "Measures without a format string render with default precision and no unit hints.",
  "FixExpression": null
}
```

- `Scope`: `Model`, `Table`, `Column`, `Measure`, `Hierarchy`, `Partition`, `Relationship`, etc.
- `Expression`: C# boolean — `true` = rule violated.
- `Severity`: 1 (Error), 2 (Warning), 3 (Info).

## Add a rule

Append to the array in `BPARules.json`. Use the appropriate `Scope`. Test with `pbir bpa run --rules BPARules.json`.

## Common custom rules

- Measures must live in a `_Measures` table, not the source table.
- Display folders required on measures.
- Lineage tags must exist on all objects.
- Measure names must not contain `_` (use spaces).
- Calculated columns must have descriptions.

## Versioning

Commit `BPARules.json` to the project repo. Treat rules as code — review changes in PRs.

## See also

- `run.md` — execute the ruleset
- [Tabular Editor's BPA rules library](https://github.com/microsoft/Analysis-Services/tree/master/BestPracticeRules) — the canonical source for community rules
