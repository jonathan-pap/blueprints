# How the `dataset` DataFrame is built

Power BI auto-creates a pandas DataFrame called `dataset` from the bound fields. The script receives it pre-loaded.

## The implicit preamble

Power BI prepends this to your script:

```python
# dataset = pandas.DataFrame(<your bound fields>)
# dataset = dataset.drop_duplicates()
```

You don't write this. You write what comes after.

## Field binding maps to DataFrame columns

Each role binding adds a column. The column name = the field's display name, not the role name.

Bind `Date.Month` to "Values" → DataFrame column is `Month`.
Bind `Sales.Revenue` to "Values" → DataFrame column is `Revenue`.

## Bind multiple fields

```bash
pbir visuals bind "<...>/MyPy.Visual" \
  -a "Values:Date.Month"   -t Column \
  -a "Values:Sales.Revenue" -t Measure
```

`dataset` then has columns `Month` and `Revenue`.

## Inspect

The script editor in Desktop shows column names in the preamble comment. Use them verbatim.

## Aggregation

Measures aggregate per categorical field automatically. To turn off aggregation (slower, larger data), there's no flag — wire your data so measures aggregate the way you want.

## Row limit

Default: 150,000 rows. Above that, Power BI sampling kicks in (and the result is non-deterministic).

## See also

- `setup.md` — make sure Python is wired up first
- `charts/*` — patterns that use `dataset`
