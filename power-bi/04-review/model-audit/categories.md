# Audit check categories (28 checks)

Full catalog ordered by severity. Use as a checklist during `audit-workflow.md` Step 2.

## Critical (block release / break model load)

1. **Bidirectional relationships** — ambiguity risk; check `crossFilteringBehavior: bothDirections` in `relationships.tmdl`
2. **Missing data types** — columns without explicit `dataType:`
3. **Circular dependencies** — between measures or tables
4. **Tables without relationships** — orphaned, unintentional

## Memory and size

5. **High-cardinality columns** — GUIDs, transaction IDs, composite keys; large dictionaries
6. **Unsplit DateTime columns** — second/millisecond precision creates near-unique dictionaries (split into Date + Time)
7. **Auto Date/Time tables** — hidden `LocalDateTable_*` / `DateTableTemplate_*` bloat; disable in Desktop Options
8. **IsAvailableInMDX on hidden / high-card columns** — wastes memory on attribute hierarchies used only by MDX (Excel PivotTables). Set `isAvailableInMDX: false`.
9. **Inappropriate data types** — Double for currency (use Fixed Decimal / Currency.Type); String for numeric
10. **Calculated columns that could be measures** — calc columns store, measures compute on demand
11. **Unused columns or tables** — no references in measures, visuals, or other consumers

## Data reduction

12. **Unfiltered history in fact tables** — no date-range filter or incremental refresh
13. **Pre-summarization opportunities** — detail grain not needed for reporting
14. **Columns better handled upstream** — calculations in calc columns or PQ that belong in the warehouse

## DAX anti-patterns

For systematic DAX query optimization, use `../../02-build/model/dax/` instead. Audit just flags presence.

15. **Filtering tables instead of columns in CALCULATE** — correctness AND performance issue
16. **Unhandled division by zero** — use `DIVIDE()` or explicit zero-check (plain `/` is fine when denominator guaranteed non-zero)
17. **Iterators with callbacks or nested iterators over large tables** — use aggregators (SUM, AVERAGE) when possible; iterators over large tables are fine if expression is SE-pushable
18. **Missing KEEPFILTERS around non-equality filter predicates in CALCULATE**

## Measure hygiene

19. **Implicit measures used where explicit measures should exist** — implicit measures are not accessible to data agents
20. **Report-scoped extension measures that should be model-level** — extension measures are invisible to data agents
21. **Duplicate or overlapping measures** — ambiguous names

## Documentation

22. **Tables or columns missing descriptions** (`///` lines in TMDL)
23. **Missing display folders for measures**
24. **Inconsistent naming conventions** — see `../../02-build/model/naming/`

## Design

25. **Star schema violations** — direct fact-to-fact relationships, snowflake patterns
26. **Missing or misconfigured date table** — must be marked (`dataCategory: Time`), continuous daily dates, span full fact range, single-column relationship. Missing any → time intelligence functions return BLANK.
27. **Excessive columns per table** — >30 suggests denormalization issues
28. **Many-to-many relationships without bridging tables**
29. **Multiple fact tables relating to the same dimension via different keys** — without conformed dimension causes slicer cross-filter gaps
30. **Inactive relationships without USERELATIONSHIP** — orphaned, suggest incomplete modeling

## Direct Lake (if applicable)

31. **Delta table health** — parquet file count (>10k = guardrail breach), V-Order enabled, row group sizes (1–16M target)
32. **DirectQuery fallback risk** — RLS definitions, SQL endpoint views trigger DQ fallback

## AI / Copilot readiness

See `ai-readiness.md` for the dedicated checklist with 7 sub-sections covering model architecture, naming + metadata, descriptions, AI instructions, AI data schema, verified answers, and data agent configuration.

Key items:

33. **Duplicate field names across tables** — confuses Copilot/data agents
34. **Missing AI instructions**
35. **Missing or inadequate descriptions for AI consumption**

## Output

For each finding: location (table/measure/relationship), problem description, specific remediation. Severity per category. Then ordered priority list.
