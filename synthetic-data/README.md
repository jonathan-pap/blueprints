# Synthetic Data Blueprint

A **folder-as-app blueprint** for creating synthetic / dummy data — schema-faithful,
statistically plausible, privacy-safe fake datasets for demos, testing, load tests, ML fixtures,
or to populate a BI model.

One blueprint inside the **Workspace-Blueprint** workspace (sibling of `power-bi/`). Follows the
3-Layer Folder Architecture: a top-level map, rooms that load only when needed, and atomic step
files that load only when their workflow runs.

## How to use

1. Point Claude (or any LLM that can read folders) at the workspace.
2. For this blueprint, read [claude.md](claude.md) — the L1 router.
3. State your intent (e.g. "generate 5,000 dummy customer rows"). Claude routes to the matching
   room and loads only the files that workflow needs.

## The pipeline

```text
01-brief  →  02-schema  →  03-generate  →  04-output  →  05-review
requirements  data shape    produce rows   serialize     validate
                                          + deliver      + privacy
```

- **Method:** tool-agnostic core, Python-first generators (Faker, numpy/scipy, optionally SDV).
- **Privacy:** synthetic only — no real data in, no real records out.
- **Reproducible:** every job records an RNG seed.

## Works alongside Power BI

`04-output/handoff-to-power-bi.md` emits generated data straight into a Power BI semantic model
(CSV-for-import or a TMDL table spliced into the `.SemanticModel`). Because `power-bi/` is a
sibling blueprint, the default target is `../power-bi/projects/<name>/` — populate a PBI model
with realistic dummy data without hunting for real source data.

## Layout

- `01-…/ … 05-…/` — numbered rooms (wiki layer)
- `projects/<name>/` — raw layer: one folder per generation job (brief + schema + generator + seed)
- `outputs/` — output layer: dated datasets (`YYYY-MM-DD-<job>-<dataset>.<ext>`)
- `_examples/` — reference snapshots (optional)

## Status

**Skeleton.** Router + room `context.md` stubs + the Power BI hand-off file are in place; atomic
step files grow per room as jobs require them. See each room's `context.md` for its roadmap.
