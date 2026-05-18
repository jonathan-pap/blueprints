# Build: fragments → monolith

Reassemble after editing serialized fragments.

## CLI

```bash
pbir theme build "<project>.Report"
```

Reads `<theme>_serialized/*` and writes the merged monolithic theme JSON back to its canonical location.

## What happens

1. CLI reads all `*.json` fragments under the serialized folder.
2. Validates each individually with `jq empty`.
3. Merges into the canonical theme JSON.
4. Writes atomically (no half-written state).

## Validate after

```bash
jq empty "<project>.Report/StaticResources/RegisteredResources/<theme>.json"
pbir validate "<project>.Report"
pbir theme colors "<project>.Report"
pbir theme text-classes "<project>.Report"
```

## Reopen Power BI Desktop

The theme JSON change is invisible to Desktop until reopen. Always close + reopen after a theme build.

## Cleanup (optional)

The serialized folder can stay alongside the monolith — useful for next-time edits. Or delete:

```bash
rm -rf "<project>.Report/StaticResources/RegisteredResources/<theme>_serialized"
```

If you delete, you'll re-run `split.md` next time you want to edit.
