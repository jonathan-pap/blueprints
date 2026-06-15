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

## Hand-authoring FillRule gradients — three traps

The `pbir visuals conditional-format` helper above emits correct JSON. But when you hand-author a
`FillRule` gradient directly (in a recipe, build script, or SVG measure), three failure modes bite:

1. **`ThemeDataColor` renders BLACK inside gradient stops.** A `min`/`mid`/`max` stop with
   `{"ThemeDataColor": …}` silently paints black. Use **`Literal` hex** for the stops — compute the
   tint from `dataColors[N]` (blend ~40–60% toward white for the min). `ThemeDataColor` is fine for
   *direct* colour (a `dataPoint.fill` solid colour, a title `fontColor`) — the trap is **stops only**.
2. **An `expr` wrapper inside a stop crashes Desktop.** Write the stop colour as
   `{"Literal":{"Value":"'#hex'"}}`, **not** `{"expr":{"Literal":…}}`. The `expr` wrapper belongs on the
   *outer* `fill.solid.color.expr.FillRule`, never inside `min.color`/`max.color`. The wrong form throws
   `Cannot read properties of undefined (reading 'accept')` in `visitFillRuleStop`.
3. **Single-series bar gradients need a wildcard selector.** Without
   `selector: {"data":[{"dataViewWildcard":{"matchingOption":0}}]}` the gradient does not render at all.
   The max stop should be the base colour at full saturation — never darker/black.

See [../references/visual-colors.md](../references/visual-colors.md) and [../schema-patterns/expressions.md](../schema-patterns/expressions.md) for the `expr` forms.

## After

`../validate/validate.md`.
