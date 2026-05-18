# Override at the wildcard level (all visuals)

Applies to every visual unless a more-specific level overrides. `visualStyles["*"]["*"]` is the wildcard slot.

## Common wildcard settings

- Disable drop shadows globally
- Default border style (color, radius)
- Default background color
- Padding around visual content

## Serialize first

```bash
pbir theme serialize "<project>.Report"
```

Find the wildcard fragment — typically `<theme>/wildcard.json`.

## Example fragment

```json
{
  "dropShadow": [{ "show": false }],
  "border": [{
    "show": true,
    "color": { "solid": { "color": "#E5E5E5" } },
    "radius": 4
  }],
  "background": [{
    "color": { "solid": { "color": "#FFFFFF" } },
    "transparency": 0
  }]
}
```

## Rebuild

```bash
pbir theme build "<project>.Report"
```

## When NOT to use wildcard

When the setting only applies to specific visual types — use `visual-type-override.md` instead. Wildcards that don't make sense for every visual create noise.

## After

`jq empty <path-to-theme>.json && pbir validate "<project>.Report"`.
