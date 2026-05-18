# How the `dataset` data.frame is built

Power BI auto-creates a `data.frame` called `dataset` from the bound fields.

## The implicit preamble

```r
# dataset <- data.frame(<your bound fields>)
# dataset <- unique(dataset)
```

You don't write this. You write what comes after.

## Field bindings → columns

Role bindings add columns named after the field display name (not the role).

`Date.Month` bound to "Values" → column is `Month`.
`Sales.Revenue` bound to "Values" → column is `Revenue`.

## Inspect

The script editor preamble lists the columns. Use them verbatim.

## Aggregation

Measures aggregate per categorical field. No flag to disable; structure your bindings so they aggregate the way you want.

## Row limit

Default 150,000 rows. Above that, Power BI samples (non-deterministic).

## Tidy data convention

R's data frames are easiest to use in long format. If you have multiple measures, consider `tidyr::pivot_longer()` to reshape before plotting.

## See also

- `setup.md` — wire R up first
- `charts/*` — patterns using `dataset`
