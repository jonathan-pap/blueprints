# model-tuning/ — Tier 3 and Tier 4 patterns

> **STOP — Requires user approval before applying any change.** Warn that model changes can break downstream reports. Suggest working on a model copy. Implement via TMDL editing (`../../`); upstream source changes (Lakehouse, Warehouse, Power Query) require Fabric CLI or pipeline coordination.

## Before applying any pattern here

1. Present specific diagnosis + proposed model change.
2. Explain why current design causes the bottleneck.
3. Run `../../../../04-review/lineage/downstream-reports.md` to assess downstream impact.
4. Suggest a model copy for experimentation.
5. Identify upstream changes required (Lakehouse / Warehouse / Power Query) — these can't be done through model tooling alone.
6. If approved, coordinate with CI/CD.
7. Re-run full baseline optimization workflow to measure impact.

## General data layout best practices

Apply at the source level — before DAX, before the SE. Both Import and Direct Lake.

- Remove unused columns and filter rows at source
- Drop all-null / all-zero fact rows that never contribute to results
- Move low-cardinality string attributes off the fact table into dimensions with integer keys
- Partition on high-filter columns (DateKey, TenantKey) so engine skips entire files; use Z-order clustering when partitioning creates too many small files
- Presort on the most filtered/grouped column first (e.g., DateKey, then ProductKey) — RLE compression improves dramatically when values cluster into longer runs per segment
- Use optimal data types — see `mdl003-data-types.md`

## Tier 3 — Model patterns (10)

- `mdl001-many-to-many.md` — bridge table layout decision matrix
- `mdl002-star-schema-conformance.md` — flatten snowflakes
- `mdl003-data-types.md` — cardinality and data type optimization
- `mdl004-aggregation-tables.md` — pre-summarized hot tables on DQ facts
- `mdl005-precompute-period-comparison.md` — physical YoY column to skip TI scan
- `mdl006-row-based-ti-table.md` — single SE scan across period measures
- `mdl007-ri-violations.md` — fix referential integrity for inner-join rewriting
- `mdl008-precomputed-booleans.md` — replace SEARCH/FIND with boolean columns
- `mdl009-historical-value-substitution.md` — collapse cardinality beyond retention window
- `mdl010-isavailableinmdx.md` — disable on disconnected slicer tables

## Tier 4 — Direct Lake (2)

- `dl001-v-ordering.md` — enable V-ordering on DL (Import has it automatically; DL does not)
- `dl002-segment-size.md` — target 1–16 M rows per rowgroup for parallelism

## Decision

Use `../decision-guide.md` "Sections 4–6 escalation triggers" to find the matching pattern.

For Direct Lake-specific work, also consult `dl001` and `dl002` independently — DL models always benefit from V-ordering and right-sized segments regardless of DAX patterns.
