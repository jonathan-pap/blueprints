# Bind Power BI data to a Deneb spec

The bound fields become a table named `dataset` accessible from the spec.

## CLI

```bash
pbir visuals bind "<...>/MyDeneb.Visual" \
  -a "Category:Date.Month"  -t Column \
  -a "Y:Sales.Revenue"      -t Measure
```

## In the spec

```json
{
  "data": { "name": "dataset" },
  "mark": "line",
  "encoding": {
    "x": { "field": "Category", "type": "temporal" },
    "y": { "field": "Y",        "type": "quantitative" }
  }
}
```

## Role naming

The role name (`Category`, `Y`, `Legend`, etc.) becomes the field name in `dataset`. Spec encodings must reference these names exactly. Rename a role → rename in the spec too.

## Aggregation

By default, measures aggregate per categorical field. To see raw rows, set `--no-aggregation` on the role binding (slow for large data; not common).

## Limits

Deneb renders client-side. Cap row count at ~5–10k for smooth rendering. Power BI's default query limit is 30k rows for custom visuals.

## See also

- `selection-signals.md` — react to Power BI cross-filters
- `spec-anatomy.md`
