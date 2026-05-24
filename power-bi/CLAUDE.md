# Power BI Desktop Workspace — Master Map

> Read this file first. It tells you which room to enter and which files to load. Do not load anything outside the row that matches the user's intent.

## What this workspace is

A reusable blueprint for working on Power BI Desktop projects (`.pbip` format). The folder IS the app — markdown + structure + the `pbir` CLI replace a custom agent.

- **Target tool:** Power BI Desktop (local)
- **File format:** PBIP (`.Report/` + `.SemanticModel/` + `.pbip`)
- **Live model connection:** rarely needed. Only when binding visuals to real measures/columns or validating DAX. See `03-bind`.
- **To see edits in PBI Desktop:** close and reopen the file. No service push needed.

## Project folder convention (raw layer)

Each Power BI project lives in `projects/<project-name>/` and follows the standard PBIP layout:

```text
projects/<project-name>/
├── <project-name>.Report/        # PBIR JSON — edit here for visuals/layout/theme
├── <project-name>.SemanticModel/ # TMDL — edit here for tables/measures/columns
└── <project-name>.pbip           # entry point opened by PBI Desktop
```

A project can be thick (model + report together) or thin (report only, connects to a remote model).

## Output convention (output layer)

Generated artifacts go in `outputs/` with strict naming:

```text
outputs/YYYY-MM-DD-<project>-<type>.md
```

Examples: `2026-05-17-sales-overview-audit.md`, `2026-05-17-sales-overview-dax-trace.log`.

## Rooms (wiki layer)

Four rooms, pipeline order. Enter one room at a time.

- `01-brief/` — Discovery, KPIs, audience, layout decisions. **No live connection.**
- `02-build/` — Edit PBIR / TMDL / theme / custom visuals. **No live connection.**
- `03-bind/` — Live model bridge for real field names, DAX validation, model edits. **Live connection.**
- `04-review/` — Validate, audit, performance, BPA, hooks. No live connection (except usage scripts).

## Folder map (current)

Counts shown as `(md files in this folder, total atomic files including subfolders)`. The tree omits `projects/`, `outputs/`, and `_examples/` (see "Layers" below for those).

```text
power-bi/
├── claude.md                                this file (L1 router)
├── README.md
├── 01-brief/                                discovery / requirements room
│   └── references/         (5 md)           vague-prompts, layout-patterns, kpi-selection, limitations, report-dev-mindset
│
├── 02-build/                                edit room — biggest, 4 sub-rooms
│   ├── report/             (2 md, 185 total)   PBIR editing — visuals, pages, bindings, formatting
│   │   ├── add-visual/     (21 md)          one file per chart type (kpi, line, bar, table, …) + templates
│   │   ├── bind/           (7  md)          find canonical names, bind/swap/clear fields
│   │   ├── layout/         (10 md)          position, size, align, page dimensions, detail gradient, guidelines, groups
│   │   ├── format/         (8  md)          override property, conditional fmt × 4 flavours, presets, apply theme
│   │   ├── schema-patterns/ (4 md)          PBIR internals — selectors, expressions, property catalogue
│   │   ├── references/     (4  md)          design best-practices — cards/KPIs, tables, colors
│   │   ├── page/           (7  md)          add / rename / delete / size / title / wallpaper
│   │   ├── filters/        (4  md)          page filter, visual filter, filter pane
│   │   ├── bookmarks/      (3  md)          create + navigator
│   │   ├── calculations/   (5  md)          visual calc, thin-report measure, ref line, error bar
│   │   ├── pbip-format/    (14 md)          PBIP file format + rename cascades + Copilot folder
│   │   ├── semantic-model/ (5  md)          read TMDL from report side (no live conn)
│   │   ├── validate/       (4  md)          pbir validate, fix broken refs, convert legacy
│   │   ├── examples/                        K201-MonthSlicer report + 55 visual.json templates
│   │   └── scripts/                         convert_legacy, background utilities
│   │
│   ├── model/              (4 md, 175+ total)  TMDL editing + DAX + Power Query + naming
│   │   ├── add/            (11 md)          measure, column, table, relationship, role, hierarchy, …
│   │   ├── update/         (3  md)          property, measure expression, multi-line DAX
│   │   ├── fix-pattern/    (7  md)          common bug recipes (summarizeBy, format, namespace collision)
│   │   ├── object-types/   (8  md)          full property reference per object
│   │   ├── naming/         (6  md)          standardize naming conventions, audit workflow, downstream impact
│   │   ├── power-query/    (19 md + 2 .py)  M authoring, query folding, validation via API/XMLA, patterns
│   │   ├── dax/            (50 md)          DAX optimization — 21 Tier-1 patterns + 4 QRY + 10 MDL + 2 DL + engine internals
│   │   └── examples/                        SpaceParts.SemanticModel (full real-world model)
│   │
│   ├── theme/              (3 md, 71 total)    theme JSON authoring + serialize/build
│   │   ├── apply/          (3  md)          template, file, copy-from-other
│   │   ├── modify/         (5  md)          colors, text classes, wildcard, visual-type override, sentiment
│   │   ├── promote/        (2  md)          lift visual-level overrides to theme
│   │   ├── audit/          (3  md)          compliance, find overrides, find hardcoded hex
│   │   ├── serialize/      (3  md)          split monolith ↔ build
│   │   ├── _deep-reference/ (1 md)          theme-json-spec (25 KB; load on explicit ask only)
│   │   └── examples/                        community theme JSONs + 49 per-visual-type override examples
│   │
│   └── visuals/            (1 md, 91 total)    custom visual engines
│       ├── deneb/          (8 md, 25 total) Vega / Vega-Lite — interactive
│       ├── svg/            (7 md, 37 total) DAX-driven SVG — in-table micro-charts
│       ├── python/         (6 md, 16 total) matplotlib / seaborn — static stats
│       └── r/              (6 md, 16 total) ggplot2 — static stats
│
├── 03-bind/                                 live model — three tiers
│   ├── via-mcp/            (11 md)          PREFERRED — Power BI MCP tool calls
│   └── via-powershell/     (19 md, 45 total) ALTERNATIVE — connect-pbid TOM/ADOMD + Enhanced Refresh REST
│       ├── tom-object-types/ (16 md)        per-object CRUD via TOM
│       └── scripts/                         PowerShell + sh + refresh_model.py
│
└── 04-review/                               validate, audit, usage, lineage, model-audit
    ├── audit/              (5 md)           report-level: full report, quick checks, design, performance
    ├── model-audit/        (7 md)           model-level: workflow, gather-context, categories, AI readiness, perf
    ├── bpa/                (2 md)           Best Practice Analyzer + custom rules
    ├── usage/              (4 md)           workspace, single report, distribution, exclude non-consumers
    ├── lineage/            (3 md + 1 .py)   downstream reports finder + other-consumer caveats
    ├── structure/          (3 md)           validate_pbip, post-rename, UTF-8 BOM check
    ├── reviewers/          (7 md)           pre-flight checklists (Deneb / SVG / Python / R / PBIP / Semantic Model Auditor)
    ├── export/             (1 md)           visual data → Excel for QA
    ├── metadata/           (1 md)           file sizes / dependencies / last-modified
    ├── hooks/                               opt-in PostToolUse validation (PBIR + TMDL + binding)
    ├── scripts/                             validate_pbip + usage scripts + get_model_info
    └── usage-metrics-dataset/               reference Power BI usage-metrics PBIP
```

## Layers (the rest of the workspace)

- **`projects/`** — raw layer. One folder per Power BI project (`<name>.Report/`, `<name>.SemanticModel/`, `<name>.pbip`). See `projects/README.md`.
- **`outputs/`** — output layer. Dated generated artifacts (`YYYY-MM-DD-<project>-<type>.<ext>`). See `outputs/README.md`.
- **`_examples/`** — upstream reference snapshot used to derive the atomic files. **Do not load unless explicitly asked.**

## Live-model preference (when you do need a live connection)

Three-tier, top to bottom:

1. **On-disk TMDL** via `pbir model -d` (`02-build/report/bind/find-canonical-name.md`). Works for thick PBIP projects. Read-only. No connection needed.
2. **Power BI MCP** (`03-bind/via-mcp/`). Preferred for everything live — queries, validation, model mutations, refresh. Clean MCP tool calls.
3. **`connect-pbid` PowerShell / TOM** (`03-bind/via-powershell/`). Alternative when MCP is unavailable, plus leverage points (field parameters, daxlib, query traces, VertiPaq stats, Parallels-on-Mac).

## Routing table

Match the user's intent. Load only what's listed.

- **New report from scratch** → `01-brief/context.md` → `02-build/context.md` → `02-build/report/context.md`
- **Add or rearrange visuals** → `02-build/report/context.md` → `add-visual/_index.md`
- **Edit a theme** → `02-build/theme/context.md`
- **Add a measure / column / table (TMDL on disk)** → `02-build/model/context.md`
- **Build a custom visual (Deneb / SVG / Python / R)** → `02-build/visuals/context.md` → pick engine
- **Bind a visual to a real measure/field** → `02-build/report/bind/find-canonical-name.md` first (no conn). If thick PBIP that's it. If thin or you need live values → `03-bind/via-mcp/` (preferred) or `03-bind/via-powershell/` (alternative).
- **Live DAX query / validation / model mutation** → `03-bind/via-mcp/` (preferred), `03-bind/via-powershell/` (alternative + leverage)
- **Optimize slow DAX** → `02-build/model/dax/_index.md` → `optimization-workflow.md` → `decision-guide.md`
- **Write / fix / validate Power Query M** → `02-build/model/power-query/_index.md`
- **Standardize naming conventions** → `02-build/model/naming/_index.md`
- **Audit a semantic model** → `04-review/model-audit/_index.md` (or dispatch `04-review/reviewers/semantic-model-auditor.md`)
- **Find downstream consumers of a model** → `04-review/lineage/downstream-reports.md`
- **Refresh a semantic model** → `03-bind/via-mcp/refresh.md` (preferred) or `03-bind/via-powershell/refresh-model.md` + `refresh-troubleshooting.md` for failures
- **Validate / audit a report** → `04-review/context.md`
- **File-format question (what is `.platform`? what is TMDL?)** → matching sub-room's atomic file only

## Loading rules

- **`claude.md` (this file) is always loaded.** Everything else is on-demand.
- **Enter one room.** When the user switches intent, drop the previous room's context before loading the new one.
- **References are leaves.** Load a `references/<topic>.md` file only when the room's `context.md` tells you to.
- **Scripts are tools.** Execute via Bash/PowerShell; do not read the whole file unless modifying it.
- **Examples are read-only artifacts.** Reference them, do not duplicate them.

## Naming conventions (strict)

- **Folders:** kebab-case, lowercase. Numbered prefix on rooms (`01-brief/`, `02-build/`) to enforce pipeline order in the file explorer.
- **Reference files:** kebab-case topic name, no date (`visual-presets.md`, `add-new-visual.md`).
- **Output files:** `YYYY-MM-DD-<project>-<type>.<ext>` (dates are absolute, never relative).
- **Project folders:** match the PBIP convention exactly — `<name>.Report`, `<name>.SemanticModel`, `<name>.pbip`.
- **No SKILL.md files.** Each room uses `context.md`. (Legacy SKILL.md files are in `_examples/` for provenance only.)

## Critical rules (apply everywhere)

- Power BI Desktop does not detect external file changes — always tell the user to close and reopen after edits.
- All PBIP files are UTF-8 **without BOM**. A BOM causes parse errors.
- Windows 260-character path limit applies — keep project roots short.
- Run `pbir validate` after every mutation in `02-build/report/`.
- **Theme-first formatting:** appearance cascades from the theme by default — the theme takes priority. Apply a visual-level override only when the user explicitly asks for that visual's customization, or it's a genuine one-off. The same override on more than 2 visuals of one type is a theme change — escalate to `02-build/theme/`. See `02-build/report/format/_index.md`.
- Never modify model metadata in `03-bind/` without explicit user direction. Always `SaveChanges()` to persist.
- Hooks in `04-review/hooks/` are opt-in — wire them per project, not globally.
- **Master hook toggle:** `power-bi/hooks.yaml` — flip `review:`, `bind:`, `outputs:`, or `briefs:` to `false` to disable a subsystem. The parent toggle wins over any per-subsystem `config.yaml`. Honor `outputs: false` by not writing audit artifacts to `outputs/`.
- **Brief auto-discovery:** if your harness has the `UserPromptSubmit` hook registered (see `01-brief/hooks/README.md`), recently-modified `projects/**/brief.md` files arrive each turn inside a `<recent-briefs>` block — read any flagged brief before asking discovery questions.
- **Canonical-name check before any binding:** run `pbir model "<project>.Report" -d` and confirm the exact `Table.Field` names BEFORE every `pbir add visual` / `pbir visuals bind` call. Do not guess from English (e.g., "Gross Profit Margin" might be `Profit %`). The `validate-visual-binding` hook (`04-review/hooks/`) blocks bindings with unknown fields, but treat it as a safety net — not the first line of defense. See `02-build/report/bind/find-canonical-name.md`.

## Provenance

This blueprint atomizes upstream community Power BI plugins into the 3-layer folder architecture. Upstream snapshot kept at `_examples/` — do not load unless explicitly asked.
