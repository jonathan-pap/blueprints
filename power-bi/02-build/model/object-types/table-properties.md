# Table properties

## Required

- `lineageTag` — unique GUID

## Categorization

- `dataCategory` — `Regular` (default), `Time` (for date tables), `Geography`, `Organization`, `BillOfMaterials`, `Accounts`

## Visibility

- `isHidden` (flag) — common for measure tables (`_Measures`) and bridge tables

## Other

- `description: '...'` or `///`
- `excludeFromModelRefresh` (flag) — skip during refresh (rare)
- `showAsVariationsOnly` (flag) — date table marked as auto date hierarchy source

## Marking as date table

```tmdl
table 'Date'
    lineageTag: <guid>
    dataCategory: Time

    column 'Date'
        dataType: dateTime
        ...
```

After saving, mark the date key column in Desktop (Modeling → Mark as date table → pick the Date column).

## Children

A `table` block contains:

- `column` (data or calculated)
- `measure`
- `hierarchy`
- `partition`
- `calculationGroup`
- `annotation` / `extendedProperty`
- `ref` (rare — model-level references)

See `../nesting-rules.md` for the full nesting matrix.
