# Power BI Desktop Workspace — Master Map

> Read this file first. It tells you which room to enter and which files to load. Do not load anything outside the row that matches the user's intent.

## What this workspace is

A reusable blueprint for working on Power BI Desktop projects (`.pbip` format). The folder IS the app — markdown + structure + the `pbir` CLI replace a custom agent.

- **Target tool:** Power BI Desktop (local)
- **File format:** PBIP (`.Report/` + `.SemanticModel/` + `.pbip`)
- **Live model connection:** rarely needed. Only when binding visuals to real measures/columns or validating DAX. See `03-bind`.
- **To see edits in PBI Desktop:** close and reopen the file. No service push needed. *(Or, if the Desktop Bridge is enabled — `desktop_bridge` in `03-bind/via-powershell/hooks/config.yaml` — reload in place + screenshot without reopening: [`03-bind/desktop-bridge.md`](03-bind/desktop-bridge.md).)*
- **Prerequisites (read once per machine):** [`00-setup.md`](00-setup.md) — the `pbir` CLI (a **community, non-commercial-licensed** tool, **not** Microsoft; needs ≥ 0.9.25), Python, Desktop, and the MS-docs links. New machine? Start there.

## Project folder convention (raw layer)

Each Power BI project lives in `projects/<project-name>/` and follows the standard PBIP layout:

```text
projects/<project-name>/
├── <project-name>.Report/        # PBIR JSON — edit here for visuals/layout/theme
├── <project-name>.SemanticModel/ # TMDL — edit here for tables/measures/columns
├── <project-name>.pbip           # entry point opened by PBI Desktop
└── design-system.yaml            # layout tokens — read before every `pbir add visual` (optional but recommended)
```

A project can be thick (model + report together) or thin (report only, connects to a remote model).

## Output convention (output layer)

Generated artifacts go in `outputs/` with strict naming:

```text
outputs/YYYY-MM-DD-<project>-<type>.md
```

Examples: `2026-05-17-sales-overview-audit.md`, `2026-05-17-sales-overview-dax-trace.log`.

## Rooms (wiki layer)

Four pipeline rooms (enter one at a time), plus a tool room.

- `01-brief/` — Discovery, KPIs, audience, layout decisions. **No live connection.**
- `02-build/` — Edit PBIR / TMDL / theme / custom visuals. **No live connection.**
- `03-bind/` — Live model bridge for real field names, DAX validation, model edits. **Live connection.**
- `04-review/` — Validate, audit, performance, BPA, hooks. No live connection (except usage scripts).

**Sibling blueprint:** bulk model ops via **Tabular Editor** (C# scripts, BPA rule sets, TE3 macros — portable TE2/TE3) live in their own top-level blueprint at [`../tabular-editor/`](../tabular-editor/CLAUDE.md). Reach for it over `03-bind/` / `02-build/model/` when changing **many** model objects at once.

## Folder map (rooms + sub-rooms)

Each room has a `context.md` (doctrine) and an `_index.md` (the file catalogue) — open those for
the per-file list; this tree is only the shape. Omits `projects/`, `outputs/`, `_examples/` (see "Layers").

```text
power-bi/
├── 00-setup.md · setup.ps1     prerequisites + bootstrap (read once per machine)
├── 01-brief/                   discovery / requirements (+ references/, wireframes/, hooks/)
├── 02-build/                   edit room — four sub-rooms
│   ├── report/                 PBIR: add-visual, bind, layout (grid tokens), format,
│   │                           page, filters, bookmarks, calculations, schema-patterns, pbip-format,
│   │                           semantic-model (read TMDL), validate, references, examples, tools (pbirkit.py + resolve_layout.py)
│   ├── model/                  TMDL: add, update, fix-pattern, object-types, naming, power-query, dax (50 patterns)
│   ├── theme/                  theme JSON: apply, modify, promote, audit, serialize, _deep-reference (spec, on ask only)
│   └── visuals/                custom engines: deneb, svg, python, r
├── 03-bind/                    live model: desktop-bridge.md · via-mcp (preferred) · via-powershell (TOM + scripts)
└── 04-review/                  audit, model-audit, bpa, usage, lineage, structure, reviewers, export, metadata,
                                hooks (opt-in PostToolUse), scripts
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
- **Plan + build a new report (guided, with approval gate)** → `01-brief/report-planning-workflow.md` (Rounds → locked `report-spec.md` → approve → build)
- **Wireframe / storyboard a report before building (story arc + low-fi page layouts, AI-drafted)** → `01-brief/wireframes/context.md` (brief → story → wireframe → review → handoff; prompts + ASCII notation)
- **How to configure a specific visual (design rules per type)** → `02-build/report/references/visual-cookbook.md`
- **Add or rearrange visuals** → `02-build/report/context.md` → `add-visual/_index.md` (read `projects/<name>/design-system.yaml` first for sizes)
- **Set up / change layout tokens (consistent sizes, grid, gaps)** → `02-build/report/layout/design-system.md`
- **Edit a theme** → `02-build/theme/context.md`
- **Add a measure / column / table (TMDL on disk)** → `02-build/model/context.md`
- **Bulk model op (format all measures, generate time-intelligence, hide keys, document the model) via a reusable script; author/run BPA rules; TE3 macros** → sibling blueprint `../tabular-editor/CLAUDE.md` (C# scripts, BPA, macros — TE2 + TE3)
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

- **`CLAUDE.md` (this file) is always loaded.** Everything else is on-demand.
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

- **Preflight the toolchain (first run / fresh clone).** Before your first `pbir`, model, or report operation in a workspace, verify the tools exist — run `pbir --version` (needs ≥ 0.9.25). If `pbir`, Python, or Power BI Desktop is missing, **STOP and prompt the user to install** — run `pwsh setup.ps1` (add `-InstallMissing` for Python/jq/Node/Desktop/Bridge CLI), or `pip install -r requirements.txt` for just `pbir` — pointing them to [`00-setup.md`](00-setup.md), and offer to run it for them. Don't attempt edits against a toolchain that isn't installed. (Visual verify via the Desktop Bridge is opt-in — `desktop_bridge` in `03-bind/via-powershell/hooks/config.yaml`. **When it's on, preflight the bridge CLI too:** `powerbi-desktop --version`, falling back to `npx -y @microsoft/powerbi-desktop-bridge-cli`; a build with the bridge on must render each page — `02-build/report/build-report.md` B9a/B10.)
- **Rooms are the workflow — not `projects/`.** When asked to build/edit, read the relevant room's atomic files (`02-build/.../*.md`) for HOW. Read only the **active** project's files (its `brief.md`, `design-system.yaml`, current `.Report/` and `.SemanticModel/`) for WHAT. Do NOT browse other `projects/<name>/` folders to crib patterns — they're user data, often stale, mid-experiment, or done in a way that wasn't best-practice. If a real worked example is needed, the rooms point to `examples/` / `_examples/` — use those. The same applies to `outputs/`: read only the active project's outputs.
- Power BI Desktop does not detect external file changes — tell the user to close and reopen after edits, **or** (if `desktop_bridge` is enabled) reload in place via `powerbi-desktop reload` (`03-bind/desktop-bridge.md`).
- All PBIP files are UTF-8 **without BOM**. A BOM causes parse errors.
- Windows 260-character path limit applies — keep project roots short.
- Run `pbir validate` after every mutation in `02-build/report/`.
- **Theme-first formatting:** appearance cascades from the theme by default — the theme takes priority. Apply a visual-level override only when the user explicitly asks for that visual's customization, or it's a genuine one-off. The same override on more than 2 visuals of one type is a theme change — escalate to `02-build/theme/`. See `02-build/report/format/_index.md`.
- **Layout-first dimensions:** size and position cascade from the project's `projects/<name>/design-system.yaml` (the dimension counterpart to the theme — Power BI themes have no width/height). Read it BEFORE every `pbir add visual`; use its 12×12 grid, per-type spans, bands, and gaps. Override a visual's dimensions only when the brief explicitly asks, or it's a one-off — and record it in the yaml `overrides:` block. The `audit-layout-consistency` hook (`04-review/hooks/`) flags off-token sizes and off-grid/sub-pixel positions. See `02-build/report/layout/design-system.md`.
- Never modify model metadata in `03-bind/` without explicit user direction. Always `SaveChanges()` to persist.
- Hooks in `04-review/hooks/` are opt-in — wire them per project, not globally.
- **Master hook toggle:** `power-bi/hooks.yaml` — flip `review:`, `bind:`, `outputs:`, or `briefs:` to `false` to disable a subsystem. The parent toggle wins over any per-subsystem `config.yaml`. Honor `outputs: false` by not writing audit artifacts to `outputs/`.
- **Brief auto-discovery:** if your harness has the `UserPromptSubmit` hook registered (see `01-brief/hooks/README.md`), recently-modified `projects/**/brief.md` files arrive each turn inside a `<recent-briefs>` block — read any flagged brief before asking discovery questions.
- **Canonical-name check before any binding:** run `pbir model "<project>.Report" -d` and confirm the exact `Table.Field` names BEFORE every `pbir add visual` / `pbir visuals bind` call. Do not guess from English (e.g., "Gross Profit Margin" might be `Profit %`). The `validate-visual-binding` hook (`04-review/hooks/`) blocks bindings with unknown fields, but treat it as a safety net — not the first line of defense. See `02-build/report/bind/find-canonical-name.md`.

## Provenance

This blueprint atomizes upstream community Power BI plugins into the 3-layer folder architecture. Upstream snapshot kept at `_examples/` — do not load unless explicitly asked.
