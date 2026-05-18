# Workspace Blueprint — Directory

> This workspace holds one or more **blueprints**. Each blueprint is a self-contained folder app for a specific tool / platform. Pick a blueprint, then read its own `claude.md` for routing.

## Workspace map

```text
Workspace-Blueprint/
├── claude.md                this file (workspace directory)
├── README.md
└── power-bi/                ── BLUEPRINT — Power BI Desktop projects (PBIP)
    ├── claude.md            entry point for this blueprint (L1 router + folder map)
    ├── README.md
    ├── 01-brief/            discovery / requirements (5 atomic files)
    ├── 02-build/            edit room — report, model (+DAX, Power Query, naming), theme, visuals (~490 atomic files)
    ├── 03-bind/             live model — Power BI MCP or PowerShell TOM + Enhanced Refresh (~50 atomic files)
    ├── 04-review/           validate, audit, model-audit, usage, lineage, reviewers (~45 atomic files + hooks + scripts)
    ├── projects/            raw layer — actual <name>.Report / <name>.SemanticModel projects
    ├── outputs/             output layer — dated artifacts YYYY-MM-DD-<project>-<type>.<ext>
    └── _examples/           provenance snapshot (do not load unless asked)
```

## Available blueprints

- **[power-bi/](power-bi/)** — Power BI Desktop projects (PBIP format). Reports, semantic models, themes, custom visuals, live-model bridge (MCP-first, PowerShell alternative), audit + validation hooks. Entry point: [power-bi/claude.md](power-bi/claude.md) (has its own detailed folder map).

## Convention for adding a blueprint

Each blueprint is a top-level kebab-case folder containing:

- `claude.md` — L1 router (rooms, routing table, hard rules)
- `README.md` — human intro + reuse instructions
- Numbered rooms (`01-brief/`, `02-build/`, …) following the 3-Layer Folder Architecture
- `projects/` — raw work (the actual files being edited)
- `outputs/` — dated generated artifacts (`YYYY-MM-DD-<project>-<type>.<ext>`)
- `_examples/` — upstream provenance snapshot (do not load unless asked)

Blueprints are self-contained — zip a blueprint folder, drop it on another machine, it still works.

## Routing rule

Match the user's intent to a blueprint. Load only that blueprint's `claude.md`. Do not browse other blueprints.
