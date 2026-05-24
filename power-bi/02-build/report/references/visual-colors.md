# Visual colors — usage best-practices

> Color encodes meaning, it doesn't decorate. The mechanics of *how* to express a color live in
> [../schema-patterns/expressions.md](../schema-patterns/expressions.md) (ThemeDataColor, FillRule, Conditional); this file is *which*
> color and *when*.

## Theme tokens over hex

Prefer theme references inside visuals; reserve literal hex for extension measures.

```json
"expr": { "ThemeDataColor": { "ColorId": 1, "Percent": 0 } }   // good — cascades with theme
"expr": { "Literal": { "Value": "'#118DFF'" } }                // avoid in visuals
```

Changing the theme then re-colors every visual and every conditional format at once.

## Semantic sentiment tokens

Use named theme tokens in conditional-format measures, not hardcoded colors:

| Token | Meaning |
|---|---|
| `good` | positive / on-target |
| `bad` | negative / off-target |
| `neutral` | unchanged / baseline |
| `minColor` / `midColor` / `maxColor` | gradient stops |

```dax
Color Measure = IF([Value] >= [Target], "good", IF([Value] >= [Target]*0.9, "neutral", "bad"))
```

Define the actual hex once in the theme (`good`/`bad`/`neutral`). If they're missing, add them
→ [../../theme/modify/sentiment-colors.md](../../theme/modify/sentiment-colors.md).

## Conditional formatting principles

1. **Theme tokens, not hex** — one change cascades everywhere.
2. **Measure-driven** — an extension measure returning tokens beats built-in gradient/rules (logic lives in one place).
3. **Sparingly** — highlight exceptions (variance/gap), never every column. Formatting everything = formatting nothing.
4. **Accessible** — blue/orange over red/green; always pair color with a secondary cue.
5. **Theme-first** — confirm sentiment colors exist before applying CF.

Patterns: positive/negative (`IF([v]>=0,"good","bad")`), gradient (`minColor→midColor→maxColor`
via FillRule), traffic-light bands (`<50% bad / 50–80% neutral / >80% good`).

## Accessibility

WCAG contrast minimums: normal text **4.5:1**, large text (18pt+) **3:1**, UI components **3:1**.
Light-gray `#AAA` on white (2.9:1) **fails**; use `#777`+ or darker.

~1% of males are red-blind (protanopia) and ~1% green-blind (deuteranopia). Safe pairings:
**blue+orange**, blue+yellow, or dark+light of one hue. Always pair color with a non-color cue —
arrow, icon, pattern, text, or marker shape.

## Don'ts

- Max 6–8 distinct colors per visual; no rainbow gradients.
- Pure black `#000` → use dark gray `#333`.
- No neon/clashing/low-contrast combos.
- Never red for positive.
- Never color as the *only* carrier of meaning.

## Related

- [../schema-patterns/expressions.md](../schema-patterns/expressions.md) — ThemeDataColor / FillRule / Conditional `expr` forms
- [../format/conditional-fmt-color-scale.md](../format/conditional-fmt-color-scale.md) — gradient CF
- [../format/conditional-fmt-rule.md](../format/conditional-fmt-rule.md) — discrete-band CF
- [../../theme/audit/find-hardcoded-hex.md](../../theme/audit/find-hardcoded-hex.md) — hunt hex that should be tokens
