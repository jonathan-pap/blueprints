# Add an action button

Clickable button for navigation, bookmarks, drill-through. No data role.

## Create

```bash
pbir add visual actionButton "<project>.Report/Overview.Page" --title "View Details" \
  --x 24 --y 600 --width 140 --height 40
```

## Configure the action

A click's behaviour lives in the **container** object `visualLink` (inside `visual`, under
`visualContainerObjects`) — not in the button's own `objects`. `type` is one of `PageNavigation`,
`Bookmark`, `Drillthrough`, `Back`, `WebUrl`, `QnA`. Because `visualLink` is a container object, any
visual can carry an action, not only buttons.

Page navigation — verified rendering and wired on the Realm Chronicle nav rail, 2026-09-13:

```json
"visualContainerObjects": {
  "visualLink": [{ "properties": {
    "show":              { "expr": { "Literal": { "Value": "true" } } },
    "type":              { "expr": { "Literal": { "Value": "'PageNavigation'" } } },
    "navigationSection": { "expr": { "Literal": { "Value": "'intro'" } } },
    "tooltip":           { "expr": { "Literal": { "Value": "'Go to Intro'" } } }
  }}]
}
```

- `navigationSection` is the target page's **name** (its folder id), not its display name.
- For a bookmark: `type: 'Bookmark'` + `bookmark: '<bookmark name>'`.
- **In Desktop, buttons need Ctrl+click** while editing; a plain click selects the visual. Readers
  in the Service click normally.
- Per-state styling uses `selector: {"id": "default"}` / `{"id": "hover"}` on `fill`, `text`,
  `icon` entries (see the template). A transparent click target laid over artwork:
  `pbirkit.nav_button()`.

## Templates

- `../examples/visuals/formatted/actionButton.json` (theme-color styled)

## See also

- `../bookmarks/bookmark-navigator.md` — built-in visual that lists ALL bookmarks; alternative to per-bookmark buttons
- `../page/_index.md` for page-navigation buttons

## After

`../validate/validate.md`.
