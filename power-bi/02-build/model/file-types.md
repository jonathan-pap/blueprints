# TMDL file types

What lives where inside `<project>.SemanticModel/definition/`.

- `model.tmdl` — Model configuration, `ref table` entries, query groups, annotations
- `database.tmdl` — Compatibility level, model ID
- `relationships.tmdl` — All relationships between tables
- `expressions.tmdl` — Shared M expressions and parameters
- `functions.tmdl` — DAX user-defined functions (reusable parameterized DAX)
- `roles/<RoleName>.tmdl` — One file per RLS / OLS role
- `perspectives/<Name>.tmdl` — One file per perspective
- `dataSources.tmdl` — Legacy data sources (modern PBI uses `expressions.tmdl` instead)
- `tables/<Name>.tmdl` — Table with columns, measures, hierarchies, partitions
- `cultures/<locale>.tmdl` — Translations + linguistic metadata

## Path-length warning

The Windows 260-character path limit bites here. Deep `tables/Some Long Table Name.tmdl` paths inside deeply-nested project folders can exceed it. Keep project root paths short.

## See also

- `nesting-rules.md` — which object types can live inside which
- `object-types/_index.md` — per-type property reference
