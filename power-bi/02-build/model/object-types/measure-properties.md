# Measure properties

## Required

- Expression after `=` (single-line or multi-line) — DAX
- `lineageTag` — unique GUID

## Display

- `formatString: '#,##0'` — static format
- `formatStringDefinition = <DAX>` — dynamic format (replaces `formatString`)
- `displayFolder: 'folder\nested'`
- `description: '...'` or `///` line above
- `isHidden` (flag)
- `isSimpleMeasure` (flag) — simple implicit-style measure

## Semantic

- `dataCategory` — string, e.g. `WebUrl`, `ImageUrl`, `BarCode`

## Format string vs definition

- Use **`formatString`** for static formats (most measures).
- Use **`formatStringDefinition`** when format depends on the measure value (signed variance, traffic-light symbols) or calculation-group context (currency switching).
- If both are present, `formatStringDefinition` wins.

## Description shortcut

`///` on the line immediately above the `measure` declaration sets `description`. Multi-line `///` concatenates. See `../fix-pattern/missing-description.md`.

## Example

```tmdl
/// Net revenue in current filter context, excluding returns.
measure 'Net Revenue' = SUM('Sales'[Amount]) - SUM('Returns'[Amount])
    formatString: #,##0
    displayFolder: 1. Revenue
    lineageTag: abc-123
```

## See also

- `../update/measure-expression.md`
- `../fix-pattern/dynamic-format-string.md`
