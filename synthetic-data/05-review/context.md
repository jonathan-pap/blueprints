# 05-review — validate, profile, privacy

> Last room before delivery. Prove the generated data satisfies the `02-schema/` contract and
> leaks no real data. A dataset that fails review is not handed off.

## Reconciliation check (config-driven jobs) — SHIPPED

For anything built with the config engine, the headline check is **marginal reconciliation** —
proof the declared `total` and `shares` actually hold in the data at every grain:

```bash
python 05-review/reconcile.py projects/<job>/config.yaml [--tol 0.01]   # exit 0 = all reconciled
```

It joins each fact to its dims and asserts every declared share (Region .40, Category .50, …) and the
grand total tie out within tolerance. This is the guarantee a bespoke generator can't offer. See
[`../03-generate/engine-share-allocation.md`](../03-generate/engine-share-allocation.md).

## Checks

- **Schema conformance** — every field present, correct type, within its declared domain.
- **Constraints & business rules** — cross-field rules hold (`end ≥ start`, `total = qty × price`).
- **Key integrity** — primary keys unique; every foreign key resolves to a parent row.
- **Distributions** — generated shape matches the schema's target (mean/spread/skew, category weights).
- **Null / edge profile** — null rates and outliers are within the declared bounds.
- **Volume** — row counts match the brief.
- **PII-leakage audit** — confirm no real records or real PII slipped through (critical for the statistical/LLM engines).

## Output of this step

A short profile/summary (and pass/fail) recorded alongside the dataset. On pass → deliver via
`../04-output/`. On fail → back to `../02-schema/` or `../03-generate/`.

## Planned atomic files (grow as needed)

- `validate-schema.md` — field/type/domain conformance
- `check-constraints.md` — business-rule + cross-field checks
- `key-integrity.md` — PK uniqueness + FK resolution
- `distribution-checks.md` — compare generated shape to target
- `pii-leakage-audit.md` — ensure synthetic-only output
- `profile-summary.md` — summary stats per dataset

## Hard rules

- No delivery without a passing review.
- PII-leakage audit is mandatory whenever the statistical or LLM engine was used.
