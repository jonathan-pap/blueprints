# The formatting cascade

Four levels. Each overrides the level above. **Read this once before any theme work.**

```
Level 1  Power BI built-in defaults
Level 2  Theme wildcard         visualStyles["*"]["*"]           → all visuals
Level 3  Theme visual-type      visualStyles["lineChart"]["*"]   → that type only
Level 4  Visual instance        visual.json objects /
                                visualContainerObjects           → wins
```

## Where to put a change

- **Applies to every visual** → Level 2 (`modify/wildcard.md`)
- **Applies to every visual of a type** → Level 3 (`modify/visual-type-override.md`)
- **One-off exception** → Level 4 (`../report/format/override-property.md`)

## Diagnosing unexpected rendering

Walk up the cascade from the visual:

1. Open the visual's `visual.json`, check `objects` / `visualContainerObjects` (Level 4).
2. Check theme `visualStyles["<type>"]["*"]` for that visual type (Level 3).
3. Check theme `visualStyles["*"]["*"]` wildcard (Level 2).
4. If unset everywhere, Power BI is applying a built-in default — set it explicitly.

## The promotion rule

If you find yourself overriding the same property on more than 2 visuals of the same type at Level 4, lift it to Level 3 via `promote/from-visuals.md`. Three identical overrides means it's a theme change in disguise.
