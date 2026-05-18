# Wildcard container defaults (`visualStyles["*"]["*"]`)

The wildcard section is the most important part of the theme — it sets the baseline for every visual before any type-specific overrides apply.

## Minimum viable wildcard

```json
"visualStyles": {
  "*": {
    "*": {
      "title": [{
        "show": true,
        "fontSize": 14,
        "fontFamily": "Segoe UI Semibold",
        "fontColor": {"solid": {"color": "#343a40"}}
      }],
      "background": [{"show": false}],
      "border": [{"show": false}],
      "dropShadow": [{"show": false}],
      "padding": [{"top": 8, "bottom": 8, "left": 8, "right": 8}]
    }
  }
}
```

## Recommended additions

- **`subTitle`** — `show: false` by default; only specific visuals should use it
- **`divider`** — `show: false` unless design calls for it
- **`visualHeader`** — `show: true` to keep the visual header (focus mode, filter icon, etc.)
- **`outspacePane`** — filter pane styling (see deep-reference for the schema)
- **`filterCard`** — filter card styling for Available and Applied states

## Design guidelines

- **`dropShadow.show: false` globally** — drop shadows create visual noise and cause vestibular issues for some users. Only enable on specific visual types that genuinely benefit.
- **`background.show: false` by default** — keeps the canvas clean. Individual visuals can opt in.
- **`border.show: false` by default** — borders are clutter. Use spacing instead.
- **Title should be enabled by default** so visuals have useful labels. Suppress per visual type as needed (e.g., textboxes).

## Color format

Container chrome colors USE the `{"solid": {"color": "..."}}` wrapper. This is the opposite of `textClasses` (which uses plain hex). The wrapper is required for `fontColor`, `background.color`, `border.color`, etc.

## After

Override critical visual types next → `visual-type-priorities.md`. The wildcard provides defaults; per-type overrides handle exceptions (textbox needs no title, etc.).

## See also

- `../modify/wildcard.md` — CLI / direct edits to wildcard after theme exists
- `../cascade.md` — the 4-level formatting cascade (level 2 = this wildcard)
