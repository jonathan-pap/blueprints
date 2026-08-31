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
├── design-system.yaml             ← OPTIONAL — layout tokens (the 12×12 grid)
├── <project-name>.Report/         ← PBIR JSON
├── <project-name>.SemanticModel/  ← TMDL
├── <project-name>.pbip            ← entry point opened in Power BI Desktop
└── build/                         ← OPTIONAL — the scripted build, if there is one
    ├── <project-name>kit.py       ←   project specifics only; imports ../../02-build/report/tools/pbirkit.py
    └── build.py                   ←   entry point, re-runnable
```

`<project-name>` is kebab-case, lowercase, no spaces. The `.Report` / `.SemanticModel` / `.pbip` suffixes are fixed by Power BI.

## Build scripts

If the report is built by script, the script is part of the project — it's how the report is
reproduced from the brief and the layout tokens. It has a fixed shape:

- **`build/<project-name>kit.py`** — only what is specific to this project (palette, fact/dimension
  table names, bespoke visual recipes). It imports the shared core at
  `../../02-build/report/tools/pbirkit.py` rather than copying from it. Typically 120–190 lines.
- **`build/build.py`** — the entry point, and it must be re-runnable: running it twice gives the same
  report. A build *step* is a function in here, not a new file.

Don't create `_build-report.py`, `build_p1.py`, `finish_build.py`, `fix_layout.py` at the project root.
One-off patch scripts are how a project ends up with a dozen of them and no way to rebuild. Full
mapping and rationale: [`../file-map.md`](../file-map.md).

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
