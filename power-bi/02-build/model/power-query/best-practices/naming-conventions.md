# Naming conventions

## Step names

- **Descriptive**: `#"Filtered Active Orders"` not `#"Custom1"`
- **Quoted identifiers**: `#"Name"` for steps with spaces (standard Power Query convention)
- Keep consistent with what the Power Query UI would generate (the UI uses friendly names automatically)

## Parameters

- **PascalCase without spaces**: `SqlEndpoint`, `DatabaseName`, `RangeStart`, `RangeEnd`
- Avoid spaces or special chars in parameter names — they propagate as `#"..."` everywhere they're referenced and add noise

## Why this matters

Power Query's UI auto-generates step names like `#"Removed Columns"`, `#"Filtered Rows"`. Manual edits like `Custom1` look out of place and obscure what each step does. The UI-generated names are good defaults.

## Examples

```m
let
    Source = Sql.Database(SqlEndpoint, Database),
    Sales = Source{[Schema="dbo", Item="Orders"]}[Data],
    #"Filtered Active" = Table.SelectRows(Sales, each [IsActive]),
    #"Selected Columns" = Table.SelectColumns(#"Filtered Active", {"OrderId", "Date", "Amount"}),
    #"Set Types" = Table.TransformColumnTypes(#"Selected Columns", {{"Amount", Currency.Type}})
in
    #"Set Types"
```

Each step name tells you exactly what it does. No `Custom1`.
