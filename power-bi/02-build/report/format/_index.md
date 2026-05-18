# format/ — atomic files

> Single-visual overrides. For changes that should apply to *all* visuals of a type, escalate to `../../theme/`.

- `override-property.md` — change one property on one visual (border, title, fonts)
- `apply-theme-to-report.md` — point the report at a different theme file
- `conditional-fmt-color-scale.md` — gradient based on value
- `conditional-fmt-data-bar.md` — in-cell bar per value
- `conditional-fmt-rule.md` — discrete colors by threshold
- `conditional-fmt-svg-icon.md` — SVG icon driven by DAX measure

## Rule

If you're about to override the same property on more than 2 visuals of the same type, stop. That's a theme change. Escalate to `../../theme/format/override-property.md` (sub-room).
