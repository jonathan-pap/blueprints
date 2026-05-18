# Serialize: monolith → fragments

Theme JSONs can hit 75 KB / 2000+ lines. Split into small editable fragments before editing.

## CLI

```bash
pbir theme serialize "<project>.Report"
```

Writes fragments to a sibling folder (e.g. `<project>.Report/StaticResources/RegisteredResources/<theme>_serialized/`).

## Fragment layout

- `dataColors.json` — palette
- `textClasses.json` — text styles
- `wildcard.json` — `visualStyles["*"]["*"]`
- `visual-types/<type>.json` — per visual type overrides (one file each)
- `meta.json` — theme name, version

See `fragment-layout.md` for full structure.

## Why split

- Tools choke on 75 KB single files.
- Diffs become meaningful (one file per logical area).
- Multiple edits don't conflict in Git.
- You can answer "what's set for line charts?" by reading 200 lines, not 2000.

## Edit cycle

1. Serialize (this step).
2. Edit specific fragment(s) — e.g. `visual-types/lineChart.json`.
3. Build → `build.md`.
4. Validate → `jq empty` + `pbir validate`.

## Don't edit the monolith between serialize/build

The serialized fragments are now the source of truth. Editing the monolith JSON desyncs them. Always re-build before any other workflow touches the report.
