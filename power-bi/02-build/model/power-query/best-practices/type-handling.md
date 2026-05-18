# Type handling

`Table.TransformColumnTypes` folds to `CAST` in SQL. Apply right after column selection.

## Pattern

```m
#"Selected" = Table.SelectColumns(Data, {"OrderId", "Date", "Amount"}),
#"Typed" = Table.TransformColumnTypes(#"Selected", {
    {"OrderId", Int64.Type},
    {"Date", type date},
    {"Amount", Currency.Type}
}),
```

Folds to: `SELECT CAST(OrderId AS bigint), CAST(Date AS date), CAST(Amount AS money) FROM ...`

## Avoid implicit type detection

Never use `Table.TransformColumnTypes` with `Replacer.ReplaceValue` or locale-dependent conversions on large datasets. These don't fold and can introduce unexpected nulls.

## Common type mappings

| M type | Use for |
|---|---|
| `Int64.Type` | Integer keys, counts |
| `type text` | Strings |
| `type date` | Date-only columns |
| `type datetime` | DateTime columns |
| `type datetimezone` | DateTime with timezone |
| `Currency.Type` | Financial amounts (Fixed Decimal) |
| `type logical` | Boolean flags |
| `Percentage.Type` | Rates, percentages |

## Common gotchas

- `Currency.Type` is Fixed Decimal — better for money than `type number` (Double) because Double has precision issues with cents and inflates dictionary cardinality.
- `type datetimezone` is rare in BI; most refresh-relevant columns are `type date` or `type datetime`.
- Avoid `type any` — disables compression optimizations.

## See also

- `../safe-pattern.md` — where types fit in the step order
- `query-folding.md` — `TransformColumnTypes` is one of the cleanest folding operations when types are compatible
- `../../object-types/column-properties.md` — model-side TMDL types these correspond to
