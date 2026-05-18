# Community examples

Inspiration libraries — browse, don't reload as full files.

- **Deneb Showcase** — https://deneb-viz.github.io/ (curated gallery of working specs)
- **Vega examples** — https://vega.github.io/vega/examples/ (general Vega gallery)
- **Vega-Lite examples** — https://vega.github.io/vega-lite/examples/ (concise charts)
- **PBI community examples** — https://community.fabric.microsoft.com/t5/Themes-Gallery/bd-p/ThemesGallery

## When to use

- "User wants a chart type I don't have a template for" → browse Vega-Lite examples first.
- "User wants something interactive" → check Deneb showcase.
- "User wants a published-paper style" → Vega examples often inspire.

## Don't paste blindly

External examples assume their own data shape. Always:

1. Rewrite `data` to `{ "name": "dataset" }`.
2. Rename encoded fields to match your role names.
3. Replace hex colors with `{ "expr": "pbiColor(N)" }`.
4. Test in Deneb's editor before saving.

## To save as a reusable example

Drop the working spec into `examples/spec/vega-lite/` or `examples/spec/vega/`. Name it descriptively (`stacked-bar-with-totals.json`). Add to `_index.md`.
