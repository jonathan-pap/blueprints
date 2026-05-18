# Add a shape

Decorative or structural rectangle / line / arrow. No data role. Use for separators, callout backgrounds, section dividers.

## Create

```bash
pbir add visual shape "<project>.Report/Overview.Page" \
  --x 24 --y 240 --width 1232 --height 2
```

## Configure shape type

In `visual.json`, set the `shape` object's `type` to one of:

- `Rectangle`
- `RoundedRectangle`
- `Oval`
- `Triangle`
- `Line` (use width or height of 1–2 px for a thin separator)
- `Arrow`

## Fill and border

```json
"objects": {
  "shape": [{
    "properties": {
      "type": { "expr": { "Literal": { "Value": "'Rectangle'" } } },
      "fill": { "solid": { "color": "#E5E5E5" } },
      "border": { "show": false }
    }
  }]
}
```

For theme-driven fill, reference `ThemeDataColor` rather than hex — see `../format/override-property.md`.

## Templates

- `../examples/visuals/formatted/shape.json`

## After

`../validate/validate.md`.
