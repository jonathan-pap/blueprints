# Visual-type override priorities

After setting the wildcard, add type-specific sections for visual types that need different defaults.

## Critical (must override — wildcard defaults don't fit)

| Visual type | Why override |
|---|---|
| `textbox` | Wildcard titles/borders don't apply to text — suppress all container chrome |
| `image` | Images rarely need a title or border |
| `shape` | Geometric shapes should have no title, background, or shadow |
| `actionButton` | Buttons have their own style system — suppress container chrome |

These four are non-negotiable. Without overrides, you get ugly default title bars on textboxes and weird borders around shapes.

## Common (often useful)

| Visual type | Common override |
|---|---|
| `kpi` | Indicator font size, trend line visibility, goal formatting |
| `card` | Category label font, value font size |
| `slicer` | Item font family/size, header font |
| `lineChart` | Legend position (`Bottom`), gridline weight |
| `tableEx` | Column header background, row alternating color |

These are nice-to-have. Add if your design calls for them.

## Pattern

In the monolithic theme:

```json
"visualStyles": {
  "*":         { "*": { /* wildcard */ } },
  "textbox":   { "*": { "title": [{"show": false}], "background": [{"show": false}], "border": [{"show": false}] } },
  "image":     { "*": { "title": [{"show": false}], "background": [{"show": false}], "border": [{"show": false}] } },
  "shape":     { "*": { "title": [{"show": false}], "background": [{"show": false}], "border": [{"show": false}], "dropShadow": [{"show": false}] } },
  "actionButton": { "*": { "title": [{"show": false}], "background": [{"show": false}] } },
  "kpi":       { "*": { /* kpi-specific */ } },
  "card":      { "*": { /* card-specific */ } }
}
```

In serialized form: each visual type lives in its own file (e.g., `textbox.json`, `kpi.json`) under the `.Theme` folder.

## Reference

`../examples/visual-types/` — 49 per-visual-type override examples covering every visual type Power BI supports. Use as a starting point for any override.

For the JSON property catalog per visual type, check the `visualStyles` section of the Power BI theme schema (see `schema-integration.md`).

## See also

- `../modify/visual-type-override.md` — CLI / pattern for adding overrides after theme exists
- `../cascade.md` — level 3 = these per-type overrides
- `../promote/from-visuals.md` — promote bespoke visual-level formatting INTO type overrides
