# projects/ — Raw layer

> One folder per Power BI project. Standard PBIP layout. This is the **raw** source the rooms operate on.

## Convention

```
projects/<project-name>/
├── brief.md                       ← OPTIONAL — project brief (single-file form)
├── brief/                         ← OPTIONAL — project brief (folder form, for bigger briefs)
│   ├── 00-context.md
│   ├── 01-kpis.md
│   └── …
├── <project-name>.Report/         ← PBIR JSON
├── <project-name>.SemanticModel/  ← TMDL
└── <project-name>.pbip            ← entry point opened in Power BI Desktop
```

`<project-name>` is kebab-case, lowercase, no spaces. The `.Report` / `.SemanticModel` / `.pbip` suffixes are fixed by Power BI.

## Project brief (recommended)

Drop a `brief.md` (or `brief/` folder for bigger projects) at the project root. The agent reads it BEFORE asking discovery questions — turns chat-only intake into a persistent, diffable, reusable record of why the report looks the way it does.

- **Template:** `../01-brief/brief-template.md` — copy this, fill the 8 sections, save as `brief.md`.
- **When to use a folder:** `../01-brief/brief-folder-structure.md`.
- **How the agent reads it:** `../01-brief/read-project-brief.md`.

When the brief exists, the agent only asks follow-ups for sections marked `[fill in]` or items under "Open questions". Comprehensive briefs = zero discovery questions.

## Thick vs thin

- **Thick** project — has both `.Report` and `.SemanticModel` folders. `definition.pbir` uses `byPath`. Self-contained.
- **Thin** project — has only `.Report`. `definition.pbir` uses `byConnection` to point at a remote model (Fabric / Power BI Service). Preferred for managed BI.

## Creating a project

From the workspace root:

```bash
cd power-bi/projects
mkdir <project-name>
cd <project-name>
pbir new report "<project-name>.Report" -c "<Workspace>/<Model>.SemanticModel"
```

`pbir` creates `<project-name>.Report/`, the bundled sqlbi theme, a default Page 1 with a title textbox, and the `.pbip` entry point.

## Multi-project workspaces

Multiple project folders can coexist here. The CLI references each by path, e.g.:

```bash
pbir validate "projects/sales-overview/Sales-Overview.Report"
pbir add visual kpi "projects/sales-overview/Sales-Overview.Report/Overview.Page" --title "Revenue"
```

## Rules

- **Do not** put generated artifacts (audits, exports, traces) in here — those belong in `../outputs/`.
- **Do not** put the workspace's reusable knowledge files in here — those belong in the rooms (`../01-brief/`, `../02-build/`, etc.).
- **UTF-8 without BOM** for every file. A BOM breaks parsers.
- Keep paths short — Windows enforces a 260-character path limit. Deep page/visual GUID nesting can blow past it.
- **PBI Desktop does not detect external file changes** — close and reopen after editing.
- Commit `.Report/` and `.SemanticModel/` to Git. Ignore `.pbix` (binary) and any local cache folders.

## Special sub-folders

- **`themes/`** — standalone theme JSONs and their serialized `.Theme/` working folders. Themes live here (not inside a single report) so they can be distributed to many reports. See [themes/README.md](themes/README.md).

## What goes here vs upstream

`_examples/` at the workspace root contains reference projects (K201-MonthSlicer, SpaceParts.SemanticModel) inside the rooms' `examples/` folders. Do not edit those — they're read-only references. Real project work lives in `projects/`.
