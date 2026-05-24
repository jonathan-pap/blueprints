# 02-schema — define the data shape

> The *definition* of what realistic fake data looks like, before any rows exist. Entities,
> fields, types, value domains, distributions, relationships, keys, and business rules. This is
> the contract `03-generate/` produces against and `05-review/` validates against.

## What it covers

- **Entities & fields** — tables/objects and their columns.
- **Types & domains** — int / decimal / string / date / bool / categorical sets / regex patterns.
- **Distributions** — uniform / normal / skewed / zipf / categorical weights; per-field.
- **Nullability & uniqueness** — null rate, unique constraints, primary keys.
- **Relationships** — 1:N, N:N, foreign keys, cardinality, referential integrity.
- **Temporal** — date ranges, trends, seasonality, ordering constraints (e.g. `end ≥ start`).
- **Business rules** — cross-field constraints (e.g. `total = qty × price`), derived fields.

## Output of this step

A `projects/<job>/schema.<ext>` (YAML/JSON/Python) the generator reads. Hand off to
`../03-generate/context.md`.

## Planned atomic files (grow as needed)

- `define-entity.md` — declare a table + its fields
- `field-types.md` — the supported field types and their parameters
- `distributions.md` — choosing + parameterizing distributions per field
- `relationships-and-keys.md` — primary/foreign keys, cardinality, referential integrity
- `business-rules.md` — cross-field constraints + derived columns
- `temporal-and-seasonality.md` — date ranges, trends, seasonal patterns
- `schema-template.md` — copy-paste schema skeleton

## Hard rules

- Schema is the single source of truth — `03-generate/` and `05-review/` both read it; don't hardcode shape in the generator.
- Declare keys + relationships here so generation can order parents before children.
