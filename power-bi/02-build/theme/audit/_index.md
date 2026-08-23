# theme/audit — find what deviates from the theme

- `compliance.md` — Audit theme compliance: Does each visual inherit from the theme cleanly, or has it accumulated bespoke overrides?
- `find-hardcoded-hex.md` — Find hardcoded hex colors: Hex colors in `visual.json` files don't follow theme color changes. Look for and replace with `ThemeDataColor`…
- `find-overrides.md` — Find visual-level overrides: List visuals that have `objects` or `visualContainerObjects` overrides — i.e., bypass the theme.
