# Reference line

A constant or measure-driven horizontal/vertical line on a chart. Use for targets, averages, thresholds.

## CLI

```bash
pbir visuals reference-line add "<...>/Visual.Visual" \
  --name "Target" \
  --value 500000 \
  --color "#2B7A78" \
  --label "Target"
```

## Measure-driven

```bash
pbir visuals reference-line add "<...>/Visual.Visual" \
  --name "1YP Avg" \
  --measure "Sales.Revenue 1YP Avg" \
  --color "#999999"
```

## Common use cases

- Sales target line
- Prior-year average line
- Capacity / threshold line ("85% utilization")
- Zero line on variance charts

## After

`../validate/validate.md`.
