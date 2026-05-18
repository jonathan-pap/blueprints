# outputs/ — Output layer

> Dated generated artifacts. Audits, exports, DAX traces, performance logs, screenshots — anything produced by a room that isn't a direct edit to a project.

## Naming convention (strict)

```
YYYY-MM-DD-<project>-<type>.<ext>
```

| Part | Rule |
|---|---|
| `YYYY-MM-DD` | Absolute date. Never relative (no "today", "yesterday"). Use the current calendar date. |
| `<project>` | The kebab-case project name (matches `../projects/<name>/`). |
| `<type>` | One of: `audit`, `usage`, `distribution`, `perf`, `trace`, `export`, `screenshot`, `validation`. Add new types only when none fit. |
| `<ext>` | Match the content: `.md` (reports), `.json`, `.csv`, `.xlsx`, `.log`, `.png`, `.svg`. |

## Examples

```
2026-05-17-sales-overview-audit.md
2026-05-17-sales-overview-usage.json
2026-05-17-sales-overview-perf.log
2026-05-17-sales-overview-export.xlsx
2026-05-17-sales-overview-screenshot-overview-page.png
```

Multiple artifacts of the same type on the same day: append a short suffix.

```
2026-05-17-sales-overview-audit-pre-rename.md
2026-05-17-sales-overview-audit-post-rename.md
```

## Which room produces what

| Room | Typical outputs |
|---|---|
| `01-brief/` | Locked brief docs (rare — usually stays in chat) |
| `02-build/` | Validation logs after `pbir validate` |
| `03-bind/` | Model exports, DAX traces, perf timings, VertiPaq stats |
| `04-review/` | Audit reports, BPA findings, usage rollups, distribution lists |

## Rules

- **Outputs are append-only.** Don't overwrite yesterday's audit — write a new dated one.
- **Don't put raw PBIP files here.** Those go in `../projects/`.
- **Don't put reusable knowledge here.** That goes in the rooms.
- Commit outputs selectively. Audits and decisions: yes. Large CSVs and logs: probably gitignore.
- If an output is a side-effect of a step in `02-build/`, link to it from the project README rather than from a room's `context.md` — rooms are stable, outputs change.
