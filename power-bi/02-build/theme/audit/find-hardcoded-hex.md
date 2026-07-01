# Find hardcoded hex colors

Hex colors in `visual.json` files don't follow theme color changes. Look for and replace with `ThemeDataColor` references.

## Audit + swap with `pbir color` (0.9.25)

The fastest path — `pbir color` audits and replaces a color across the **whole report *and* its theme**
in one pass (visual properties, the visual container, page/canvas background, conditional-formatting
stops/cases, and the theme palette). Needs **≥ 0.9.25** (`pip install -U pbir-cli`; community tool,
non-commercial license — see [`../../../00-setup.md`](../../../00-setup.md)):

```bash
pbir color list "<project>.Report"                                     # audit: distinct colors + usage counts (report + theme)
pbir color replace "<project>.Report" --from "#FF0000" --to "#00FF00"  # PREVIEW (dry-run is the default)
pbir color replace "<project>.Report" --from "#FF0000" --to "#00FF00" -f          # apply everywhere (--force)
pbir color replace "<project>.Report" --from "#FF0000" --to "#00FF00" --theme     # scope: theme palette only
pbir color replace "<project>.Report" --from "#FF0000" --to "#00FF00" --report    # scope: report colors only
```

`color list` is the re-theming/brand-swap audit; `color replace` is the bulk fix. It swaps the literal
hex — for **theme-following** colors you still want `ThemeDataColor` references (below).

## Grep (manual fallback, or on < 0.9.25)

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
