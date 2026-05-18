# Room 02 — Build

> Edit the PBIP project files. No live model connection from this room (that's `../03-bind/`). Power BI Desktop will pick up changes when the user closes and reopens the file.

## When to enter

User has a locked brief (from `../01-brief/`) and wants to actually modify report/model/theme/visual files.

## Sub-room router

Match the task to one sub-room. Enter one sub-room at a time. Each sub-room has its own `context.md` and `references/`.

| Task | Sub-room |
|---|---|
| Add / move / format / bind visuals; create pages; edit layout | `report/` |
| Add or change measures, columns, tables, relationships, hierarchies | `model/` |
| Change colors, fonts, default styles for all visuals of a type | `theme/` |
| Build a custom visual that native Power BI can't express | `visuals/` then pick engine |

## Decision rules

- **Theme vs visual override:** If the change should apply to every visual of a type, edit `theme/`. If it's a single-visual exception, edit `report/`.
- **Model vs report extension:** If the measure is reusable, add it to the model via `model/`. If it's report-specific only, add a thin-report measure via `report/references/thin-report-measures.md`.
- **Native vs custom visual:** Try native visuals first. Only enter `visuals/` when native cannot express the chart.
- **Need real field/measure names?** Stop. Load `../03-bind/context.md`, get the names, come back.

## Hard rules across all sub-rooms

- All PBIP files are **UTF-8 without BOM**. A BOM breaks parsers.
- After every mutation in `report/`, run `pbir validate "<project>.Report"`.
- After every mutation in `model/`, validate TMDL syntax (see `model/context.md`).
- Never edit `.pbi`/`.platform` files unless explicitly intended — they carry IDs.
- Renames cascade: a table or measure rename touches TMDL, visual JSON, report extensions, culture files, and DAX query files. See `report/references/rename-patterns.md` and `model/references/naming-conventions.md`.
- Tell the user to close and reopen Power BI Desktop after the change — it does not detect external file edits.

## Project layout you're editing

```
projects/<name>/
├── <name>.Report/         ← report/ sub-room writes here
├── <name>.SemanticModel/  ← model/ sub-room writes here
└── <name>.pbip
```

The theme JSON lives inside `<name>.Report/StaticResources/`. Custom visuals (Deneb/SVG/Python/R) are wired through `<name>.Report/` visual.json files but their source artifacts live alongside the project.

## Outputs

This room produces edits in `projects/<name>/`. Any generated artifacts (audit logs, DAX traces, exports) belong in `../outputs/` with `YYYY-MM-DD-<project>-<type>.<ext>` naming.
