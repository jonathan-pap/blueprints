# Relationship properties

## Required

- Identifier (typically a GUID after `relationship`)
- `fromColumn: 'Table'.Column`
- `toColumn: 'Table'.Column`

## Cardinality

- `fromCardinality` — `none`, `one`, `many`
- `toCardinality` — `none`, `one`, `many`

Common pattern: fact → dim is `fromCardinality: many`, `toCardinality: one`.

## Filtering

- `crossFilteringBehavior` — `oneDirection` (default), `bothDirections`, `automatic`
- `securityFilteringBehavior` — `oneDirection`, `bothDirections`, `none`

## State

- `isActive` (flag) — default true. Omit the line for default; include `isActive: false` to mark inactive.

## Example

```tmdl
relationship abc123-def456-ghi789
    fromColumn: 'Sales'.CustomerID
    toColumn:   'Customers'.CustomerID
    fromCardinality: many
    toCardinality:   one
    crossFilteringBehavior: oneDirection
```

## Bidirectional warning

`bothDirections` enables filter propagation in both directions. Useful for many-to-many bridge tables but can cause ambiguity and slow query plans. Use deliberately.

## Active vs inactive

Only one active relationship per pair of tables. Use inactive relationships with `USERELATIONSHIP()` in DAX for alternate paths (e.g. `OrderDate` vs `ShipDate` to a single `Date` table).
