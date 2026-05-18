# Find hardcoded hex colors

Hex colors in `visual.json` files don't follow theme color changes. Look for and replace with `ThemeDataColor` references.

## Grep

```bash
grep -rE "'#[0-9A-Fa-f]{6}'" "<project>.Report/definition/pages/"
```

## What's OK

- Hex in **extension measures** (`reportExtensions.json`) that return sentiment colors — they're already abstracted via the `good`/`bad`/`neutral` mapping.
- Hex in **theme JSON** itself — that's where colors are supposed to live.

## What to fix

Hex literals in **visual.json** `objects` / `visualContainerObjects`. Replace:

```json
// Bad — hardcoded
"expr": {"Literal": {"Value": "'#118DFF'"}}

// Good — references theme palette
"expr": {"ThemeDataColor": {"ColorId": 1, "Percent": 0}}
```

`ColorId` is 1-based. `Percent` is shade adjustment.

## Lift sentiment colors

If you find hex literals being used for "red = bad" patterns, move them to the theme's sentiment colors (`../modify/sentiment-colors.md`) and use extension measures returning `"bad"` instead.

## After

`../../report/validate/validate.md` after replacement.
