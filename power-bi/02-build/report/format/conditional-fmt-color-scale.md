# Conditional formatting — color scale

Continuous gradient based on a measure value. Use for variance columns in tables, heatmap-style matrices.

## Apply

```bash
pbir visuals conditional-format "<...>/Visual.Visual" \
  --target "Sales.Revenue" \
  --type colorScale \
  --min-color "#FFFFFF" --max-color "#2B7A78"
```

## With theme-driven colors (preferred)

Use theme sentiment colors so re-theming propagates:

```bash
pbir visuals conditional-format "<...>/Visual.Visual" \
  --target "Sales.Variance" \
  --type colorScale \
  --min-color "themedataColor.bad" --max-color "themedataColor.good"
```

## When to use

- Variance / delta columns
- Heatmap matrices
- Performance vs target

## When NOT to use

- Already a color-encoded measure
- Sparse data (most cells empty)
- Primary measure column (color the GAP not the value)

## After

`../validate/validate.md`.
