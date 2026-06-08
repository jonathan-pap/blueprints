# Add a relationship (TMDL)

Edit `<project>.SemanticModel/definition/relationships.tmdl`. Each relationship is a root-level `relationship` block.

## Pattern

```tmdl
relationship abc123-def456-ghi789
    fromColumn: 'Sales'.CustomerID
    toColumn:   'Customers'.CustomerID
    fromCardinality: many
    toCardinality:   one
    crossFilteringBehavior: oneDirection
```

## Required

- Name: a unique identifier (typically a GUID).
- `fromColumn` and `toColumn` in `'Table'.Column` form.
- `fromCardinality` and `toCardinality` (defaults to many/one for typical fact→dim).

## Optional

- `crossFilteringBehavior`: `oneDirection` (default), `bothDirections`, `automatic`
- `securityFilteringBehavior`: `oneDirection`, `bothDirections`, `none`
- `isActive`: bare keyword to flag the relationship as active (default true)

Write `isActive` alone to mark inactive — actually, omit the line. The presence of the keyword toggles depending on context; safest is to test with both shapes if uncertain.

## Inactive relationship example

```tmdl
relationship xyz789-abc123-def456
    fromColumn: 'Sales'.ShipDate
    toColumn:   'Date'.Date
    isActive: false
```

## Bidirectional warning

`crossFilteringBehavior: bothDirections` is powerful but can cause ambiguity and performance issues. Use only when needed (typically for many-to-many bridge tables).

## Pitfall — ambiguous filter paths (two active paths between the same two tables)

Power BI refuses to load with *"ambiguous paths between X and Y"* whenever a fact can reach a dimension via two **active** relationship paths — e.g. `fct → dim` directly AND `fct → bridge → dim`. This is structural; cosmetic fixes don't work. Only one active path between any pair of tables is allowed.

The fix:

1. Pick the path that should drive **default** filtering (usually the one most visuals depend on). Leave that `isActive: true`.
2. Mark every other path between the same two tables `isActive: false`.
3. In measures that need an inactive path, wrap `CALCULATE` with `USERELATIONSHIP(from, to)`:

   ```dax
   # Received-by-date =
   CALCULATE (
       COUNTROWS ( fct_delivery ),
       USERELATIONSHIP ( fct_delivery[received_date], dim_calendar[Date] )
   )
   ```

   The inactive relationship is dormant until a measure activates it locally, so the model has a single active path overall.

The common case is a fact with multiple date columns (received, shipped, invoiced): pick one to be the default calendar relationship, deactivate the rest, then write `# Received-by-date`, `# Shipped-by-date`, etc. measures that swap in via `USERELATIONSHIP`.

Confirmed 2026-05-19 against gddt — adding an active `fct_delivery[received_date] → dim_calendar[Date]` while the indirect path `fct_delivery → expected[period_date] → dim_calendar` was already active blocked the model.

## After

`bash ../../../04-review/hooks/validate-tmdl.sh "<project>.SemanticModel"`. Reopen Desktop.
