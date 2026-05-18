# Add an action button

Clickable button for navigation, bookmarks, drill-through. No data role.

## Create

```bash
pbir add visual actionButton "<project>.Report/Overview.Page" --title "View Details" \
  --x 24 --y 600 --width 140 --height 40
```

## Configure the action

In `visual.json`, set the `actionButton` object's `action.type` to one of:

- `Bookmark` — switch to a named bookmark
- `PageNavigation` — jump to another page
- `DrillThrough` — drill to a target page filtered by current context
- `WebUrl` — open an external link
- `QnA` — open Power BI Q&A overlay

Example bookmark action:

```json
"objects": {
  "actionButton": [{
    "properties": {
      "action": {
        "type": "Bookmark",
        "bookmark": "Quarterly View"
      }
    }
  }]
}
```

## Templates

- `../examples/visuals/formatted/actionButton.json` (theme-color styled)

## See also

- `../bookmarks/bookmark-navigator.md` — built-in visual that lists ALL bookmarks; alternative to per-bookmark buttons
- `../page/_index.md` for page-navigation buttons

## After

`../validate/validate.md`.
