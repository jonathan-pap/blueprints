# Workspace Blueprint — Directory

> This workspace holds one or more **blueprints**. Each blueprint is a self-contained folder app for a specific tool / platform. Pick a blueprint, then read its own `CLAUDE.md` for routing.

## Workspace map

```text
Workspace-Blueprint/
├── CLAUDE.md                this file (workspace directory)
├── README.md
├── briefs/                  ── HUB — brief templates (linked) + filled examples (NOT a blueprint)
│   ├── README.md            how to use; links to each blueprint's canonical template
│   └── examples/            filled example briefs (power-bi + synthetic-data, a paired set)
├── power-bi/                ── BLUEPRINT — Power BI Desktop projects (PBIP)
│   ├── CLAUDE.md            entry point for this blueprint (L1 router + folder map)
│   ├── README.md
│   ├── 01-brief/            discovery / requirements (5 atomic files)
│   ├── 02-build/            edit room — report, model (+DAX, Power Query, naming), theme, visuals (~490 atomic files)
│   ├── 03-bind/             live model — Power BI MCP or PowerShell TOM + Enhanced Refresh (~50 atomic files)
│   ├── 04-review/           validate, audit, model-audit, usage, lineage, reviewers (~45 atomic files + hooks + scripts)
│   ├── projects/            raw layer — actual <name>.Report / <name>.SemanticModel projects
│   ├── outputs/             output layer — dated artifacts YYYY-MM-DD-<project>-<type>.<ext>
│   └── _examples/           provenance snapshot (do not load unless asked)
└── synthetic-data/         ── BLUEPRINT — synthetic / dummy data creation (Python-first)
    ├── CLAUDE.md            entry point for this blueprint (L1 router + folder map)
    ├── README.md
    ├── 01-brief/            requirements — what data, volume, seed, PII policy
    ├── 02-schema/           define the data shape — entities, types, distributions, rules
    ├── 03-generate/         generation engines — faker / distribution / relational / statistical / LLM
    ├── 04-output/           serialize & deliver (CSV/JSON/Parquet/SQL/DB + Power BI hand-off)
    ├── 05-review/           validate, profile, key integrity, PII-leakage audit
    ├── projects/            raw layer — one folder per generation job
    └── outputs/             output layer — dated datasets YYYY-MM-DD-<job>-<dataset>.<ext>
```

## Available blueprints

- **[power-bi/](power-bi/)** — Power BI Desktop projects (PBIP format). Reports, semantic models, themes, custom visuals, live-model bridge (MCP-first, PowerShell alternative), audit + validation hooks. Entry point: [power-bi/CLAUDE.md](power-bi/CLAUDE.md) (has its own detailed folder map).
- **[synthetic-data/](synthetic-data/)** — synthetic / dummy data creation (Python-first: Faker, numpy/scipy, SDV). Schema-faithful, privacy-safe fake datasets for demos, testing, ML fixtures, or to populate a BI model. Includes a Power BI hand-off that writes generated data into a `power-bi/` semantic model. Entry point: [synthetic-data/CLAUDE.md](synthetic-data/CLAUDE.md). *(Skeleton — rooms grow per job.)*

## Convention for adding a blueprint

Each blueprint is a top-level kebab-case folder containing:

- `CLAUDE.md` — L1 router (rooms, routing table, hard rules)
- `README.md` — human intro + reuse instructions
- Numbered rooms (`01-brief/`, `02-build/`, …) following the 3-Layer Folder Architecture
- `projects/` — raw work (the actual files being edited)
- `outputs/` — dated generated artifacts (`YYYY-MM-DD-<project>-<type>.<ext>`)
- `_examples/` — upstream provenance snapshot (do not load unless asked)

Blueprints are self-contained — zip a blueprint folder, drop it on another machine, it still works.

## Brief intake hub

[`briefs/`](briefs/) is a shared, non-blueprint hub: it links to each blueprint's canonical brief
template and holds **filled example briefs** to learn from. Start there to pick a template, then
save the filled brief to the target blueprint's `projects/<name>/brief.md` — where that blueprint's
discovery hook picks it up. See [briefs/README.md](briefs/README.md).

## Routing rule

Match the user's intent to a blueprint. Load only that blueprint's `CLAUDE.md`. Do not browse other blueprints. `briefs/` is a hub, not a blueprint — the filled brief always lands under a blueprint's `projects/`.
