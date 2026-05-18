# Promote visual-level formatting into the theme

When 3+ visuals of the same type share an override, lift it to a theme-level rule. Cleaner visual JSON, single source of truth, easier rebranding.

## Procedure

1. **Find the candidates:**

```bash
pbir audit overrides "<project>.Report" --by visual-type
```

Returns each visual-type with the count of overridden properties across visuals.

2. **Pick a property that's overridden on most visuals of a type.** E.g., `title.fontSize = 14` set on 8 of 10 line charts.

3. **Add it to the theme** at the visual-type level — see `../modify/visual-type-override.md`.

4. **Clear the now-redundant overrides** from each visual — see `clear-visual-overrides.md`.

5. **Verify** — visuals should still render identically. The theme now provides the formatting; visuals reference rather than redefine.

## Example

10 line charts each have `objects.title[0].properties.fontSize.expr.Literal.Value = "14"`.

After promotion:
- Theme `visualStyles["lineChart"]["*"].title = [{ "fontSize": 14, "show": true }]`
- Each line chart's `visual.json` loses the per-visual title override

Result: same rendering, ~10 lines removed per visual, single place to change.

## Don't over-promote

A property unique to one visual stays in `visual.json`. Promote only when it generalizes.

## After

`../../report/validate/validate.md`. Reopen Desktop and check every promoted visual still renders correctly.
