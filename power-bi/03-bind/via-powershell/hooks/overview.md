# Hook overview — what fires and when

5 hooks, 2 events. All triggered by Bash commands matching the `if` filter in `hooks.json`.

| Hook | Event | `if` filter | What it does |
|---|---|---|---|
| `validate-dax` | PreToolUse | `Bash(*tom_nuget*)` or `Bash(* -File *.ps1*)` | Parses DAX `'Table'[Column]` and `[Measure]` refs from the command (or referenced `.ps1` file). Checks each against the cached model metadata (`tmp/model-metadata.json`). Suggests close matches on miss. **Blocks (exit 2)** if a reference is invalid. |
| `validate-measure` | PreToolUse | `Bash(*Measures.Add*)` or `Bash(* -File *.ps1*)` | Requires every `.Measures.Add(...)` call to set `DisplayFolder`, `Description`, and `FormatString` (or `FormatStringDefinition`). **Blocks (exit 2)** if any are missing. |
| `refresh-cache` | PostToolUse | `Bash(* -File *.ps1*)` (filters internally) | After any TOM connect or modification (`SaveChanges`, `.Measures.Add`, `.Columns.Add`, etc.), re-runs `snapshot-model.ps1` to refresh `tmp/model-metadata.json` so subsequent `validate-dax` calls see current state. |
| `check-ri` | PostToolUse | `Bash(*SaveChanges*)` | Runs `check-referential-integrity.ps1` against the live model. Reports unmatched many-side keys, silent M:M exclusions, and "Assume RI" risks. **Blocks (exit 2)** on any violation. |
| `check-compat` | PostToolUse | `Bash(* -File *.ps1*)` | Compares model `CompatibilityLevel` to the engine's max. If lower, lists the features available by upgrading. Optionally auto-upgrades if `compatibility_auto_upgrade: true`. Suppresses repeats via a marker file. |

## Cache contract

- **Producer**: `snapshot-model.ps1` (invoked by `refresh-cache` hook). Writes `<project>/tmp/model-metadata.json` with `{port, database, compatibilityLevel, maxCompatibilityLevel, snapshotTime, tables: [{name, columns, measures}]}`.
- **Consumers**: `validate-dax`, `check-ri`, `check-compat` all read `tmp/model-metadata.json`. If absent, hooks **skip silently** (exit 0) — never block on missing cache.

## Exit conventions

- `0` — OK or not applicable (e.g., filter didn't match, cache missing, jq missing)
- `2` — blocking error; stderr is shown to Claude as a tool-use rejection

Hooks NEVER use `set -u` and defensively exit 0 on environmental failures (no jq, no PowerShell, malformed cache, etc.). The cost of a false-positive block is much higher than a missed validation.

## See also

- `config.md` — toggle individual checks
- `windows-issues.md` — why hooks may not fire on Windows + the master kill-switch
- `../snapshot-model.ps1`, `../check-referential-integrity.ps1` — the PowerShell payloads
