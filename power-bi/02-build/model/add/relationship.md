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

## After

`bash ../../../04-review/hooks/validate-tmdl.sh "<project>.SemanticModel"`. Reopen Desktop.
