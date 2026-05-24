# Synthetic Data Blueprint — Master Map

> Read this file first. It routes you to the right room and tells you which files to load.
> The folder IS the app — markdown + structure + small Python generators replace a custom agent.
> Do not load anything outside the row that matches the user's intent.
>
> This is one blueprint inside the **Workspace-Blueprint** workspace (sibling of `power-bi/`).
> The workspace-level `../CLAUDE.md` routes between blueprints; this file routes within this one.

## What this is

A reusable blueprint for **creating synthetic / dummy data** — schema-faithful, statistically
plausible, privacy-safe fake datasets for demos, testing, load tests, ML fixtures, or to
populate a BI model.

- **Method:** tool-agnostic core, **Python-first** generators (Faker, numpy/scipy distributions, optionally SDV when mimicking the shape of a real dataset).
- **No real data in, no real data out** — synthetic only. See Critical rules.

## Project folder convention (raw layer)

Each generation job lives in `projects/<job-name>/`:

```text
projects/<job-name>/
├── brief.md            what data, why, volume, seed, output target
├── schema.<ext>        the data definition (entities, fields, distributions, rules)
├── generate.py         the generator script
└── seed.txt            recorded RNG seed for reproducibility
```

## Output convention (output layer)

```text
outputs/YYYY-MM-DD-<job>-<dataset>.<ext>
```

Example: `outputs/2026-05-24-demo-financials.csv`. Dates are absolute, never relative.

## Rooms (pipeline order — enter one at a time)

- `01-brief/`    — requirements: what data, purpose, volume, seed, PII policy, output target
- `02-schema/`   — define the data shape: entities, fields, types, distributions, relationships, rules
- `03-generate/` — pick an engine and produce rows (faker / rule / distribution / relational / statistical / LLM)
- `04-output/`   — serialize & deliver (CSV / JSON / Parquet / SQL / DB + Power BI hand-off)
- `05-review/`   — validate, profile, check keys + constraints, PII-leakage audit

## Folder map

```text
synthetic-data/
├── CLAUDE.md                 this file (L1 router)
├── README.md
├── 01-brief/      (context.md)   discovery / requirements
├── 02-schema/     (context.md)   define the data shape
├── 03-generate/   (context.md)   generation engines + execution
├── 04-output/     (context.md)   serialize & deliver (+ handoff-to-power-bi.md)
├── 05-review/     (context.md)   validate, profile, privacy
├── projects/                     raw layer — one folder per generation job
├── outputs/                      output layer — dated datasets
└── _examples/                    reference snapshots (optional; do not load unless asked)
```

> Skeleton stage: each room currently has a `context.md` describing its purpose and a roadmap of
> the atomic files it will grow. Fill rooms incrementally as jobs demand them.

## Routing table

Match the user's intent. Load only what's listed.

- **New dataset from scratch** → `01-brief/context.md` → `02-schema/context.md` → `03-generate/context.md`
- **Define or change the schema** → `02-schema/context.md`
- **Pick / configure a generation engine** → `03-generate/context.md`
- **Export to a format or load to a database** → `04-output/context.md`
- **Generate data for a Power BI model** → `04-output/handoff-to-power-bi.md`
- **Validate / profile a generated dataset** → `05-review/context.md`
- **Mimic the shape of a real dataset (privacy-safe)** → `02-schema/context.md` → `03-generate/context.md` (statistical engine)

## Loading rules

- **`CLAUDE.md` (this file) is always loaded.** Everything else is on demand.
- **Enter one room.** Drop the previous room's context when intent changes.
- **Scripts are tools.** Run them; don't read a whole script unless modifying it.
- **Examples are read-only.** Reference, don't duplicate.

## Naming conventions (strict)

- **Folders:** kebab-case, lowercase; numbered prefix on rooms (`01-brief/`, `02-schema/`) to enforce pipeline order.
- **Room files:** each room uses `context.md` (no SKILL.md). Atomic files are kebab-case topic names, no date.
- **Output files:** `YYYY-MM-DD-<job>-<dataset>.<ext>` (absolute dates).

## Critical rules (apply everywhere)

- **Synthetic only.** Never embed, copy, or output real PII or real records. When mimicking a real dataset, learn its *distributions and structure* — never copy rows through.
- **Reproducible.** Always set and record an RNG seed (`seed.txt`). Same seed + same schema = same data.
- **Schema before generation.** Define `02-schema/` before running `03-generate/`.
- **Referential integrity.** Generate parent tables before children; every foreign key must resolve.
- **Validate before delivery.** Run `05-review/` against the schema before handing data off.
- **Volume-aware.** Batch / stream large volumes; don't hold millions of rows in memory.
- **Power BI hand-off writes into a Power BI project folder** — by default the sibling `../power-bi/projects/<name>/<name>.SemanticModel/`, or any path you supply. Confirm the destination before writing.
