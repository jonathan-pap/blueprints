# Thick vs Thin

| | Thick | Thin |
|---|---|---|
| Has `.SemanticModel/`? | Yes | No |
| Has `.Report/`? | Yes | Yes |
| `definition.pbir` `byPath` or `byConnection` | `byPath` (local) | `byConnection` (remote model) |
| Use when | Self-contained, exploratory | Managed BI, shared model |

How to tell at a glance: list the project folder. If you see `<name>.SemanticModel/`, it's thick. If not, it's thin.

For thin projects, the remote model must already exist in Fabric / Power BI before the report can open.
