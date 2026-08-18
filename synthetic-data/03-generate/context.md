# 03-generate — generation engines + execution

> Pick an engine and produce rows against the `02-schema/` definition. Most jobs combine engines
> (Faker for identity fields, distribution sampling for numerics, relational wiring for keys).

## Default path — the config-driven star engine (SHIPPED)

For any **dimensional (star-schema) dataset**, don't hand-write a generator. Declare dims + facts +
measures with `total`/`shares` in a YAML config and run the reusable engine:

```bash
python 03-generate/generate.py projects/<job>/config.yaml   # -> Dim*/Fact* + _manifest.json
python 05-review/reconcile.py  projects/<job>/config.yaml   # proves marginals tie out
```

- **Config grammar:** [`../02-schema/config-schema.md`](../02-schema/config-schema.md) · template
  [`../02-schema/schema-template.yaml`](../02-schema/schema-template.yaml)
- **How allocation + raking works:** [`engine-share-allocation.md`](engine-share-allocation.md) — declare
  top-line totals and shares per dimension/attribute; the engine allocates top-down and rakes so every
  marginal reconciles at every granularity (day/month/region/product…).
- **Multi-domain:** retail, telecom, finance, web — same engine, different config.

Reach for the bespoke engines below only for **non-dimensional** data (a single flat table of realistic
text/records) or shapes the config grammar can't express yet.

## Engines

| Engine | Use for |
|---|---|
| **Faker** | realistic identity/text fields — names, addresses, emails, companies, locale-aware |
| **Rule-based** | derived/computed fields and business rules (`total = qty × price`) |
| **Distribution sampling** | numeric fields with a target shape (numpy/scipy: normal, skew, zipf…) |
| **Relational** | parent→child generation with resolving foreign keys + cardinality |
| **Statistical (SDV)** | mimic the *shape* of a real dataset without copying rows (copulas, CTGAN) |
| **LLM** | small volumes of realistic free text / edge cases where templates fall short |

## Execution concerns

- **Seeding** — set + record the RNG seed (`projects/<job>/seed.txt`) so runs are reproducible.
- **Order** — generate parent tables before children so foreign keys resolve.
- **Edge cases & nulls** — inject controlled null rates, outliers, duplicates per the schema.
- **Scaling** — batch/stream for large volumes; don't hold everything in memory.

## Output of this step

In-memory rows / staged files ready for `../04-output/context.md` to serialize. Validate with
`../05-review/context.md` before delivery.

## Planned atomic files (grow as needed)

- `engine-faker.md`, `engine-rule-based.md`, `engine-distribution-sampling.md`,
  `engine-relational.md`, `engine-statistical-sdv.md`, `engine-llm.md`
- `seeding-reproducibility.md` — set + record seeds
- `scaling-performance.md` — batching, streaming, memory
- `edge-cases-and-nulls.md` — controlled imperfections
- `generate-template.py` — generator skeleton reading `schema.<ext>`

## Hard rules

- Honor the schema; don't invent fields the schema didn't declare.
- Record the seed for every run.
- Statistical engine: learn distributions, never pass real rows through to output.
