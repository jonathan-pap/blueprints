# schema-patterns/ — atomic files

> The PBIR formatting internals: how a property is *expressed*, *scoped*, and *found*. Load these
> when hand-authoring `visual.json` formatting (recipes, build scripts) or debugging why a
> conditional format won't render.

- `selectors.md` — when/what a property applies to (`dataViewWildcard` matchingOption, `metadata:"select"`, `scopeId`, `roles`, element `id` states; the two-entry pattern)
- `expressions.md` — what goes inside `expr` (literal suffix/quote rules, Measure/Column/ThemeDataColor, FillRule gradients, Conditional bands, SourceRef context)
- `property-catalogue.md` — `pbir schema` discovery commands + universal containers + per-type container index for all 49 visual types

## When you need this

| Task | Start here |
|---|---|
| "What's the exact property name for X?" | `property-catalogue.md` → `pbir schema describe` |
| "Why is my conditional color all one shade?" | `selectors.md` (matchingOption 1 vs 0) |
| "Measure not found / value ignored" | `expressions.md` (Schema:extension, suffix/quote rules) |
| Hand-authoring a recipe's `visual.json` | all three |
