# 01-brief — discovery / requirements

> First room. Pin down **what data, for what, and under what constraints** before designing or
> generating anything. Output of this room is a `projects/<job>/brief.md` the later rooms read.

## What to gather

- **Purpose** — demo / functional test / load test / ML fixture / populate a BI model. Drives realism + volume.
- **Datasets & volume** — which entities/tables, how many rows each, growth over time.
- **Schema source** — from scratch, match an existing schema, or mimic a real dataset's shape.
- **Realism level** — random-but-valid vs. business-plausible distributions/correlations.
- **Locale / language** — names, addresses, currency, date formats.
- **Reproducibility** — seed required? (default: yes — record it.)
- **PII policy** — synthetic only; confirm no real records may be used as input or output.
- **Output target** — file format + destination (filesystem / DB / Power BI model).

## Output of this step

A `projects/<job>/brief.md`: purpose, entity list + row counts, realism level, locale, seed,
PII note, output target. Hand off to `../02-schema/context.md`.

## Planned atomic files (grow as needed)

- `brief-template.md` — copy-paste template for `projects/<job>/brief.md`
- `references/use-cases.md` — demo vs test vs load vs ML, and how each shifts realism/volume
- `references/volume-and-seeding.md` — sizing guidance + why/how to fix a seed
- `references/pii-policy.md` — the synthetic-only rule, mimicking real data safely

## Hard rules

- No real PII or real records as input. If "make it look like our prod data," mimic the *shape*, never copy rows (see `../03-generate/` statistical engine).
- Don't proceed to schema until purpose + volume + output target are known.
