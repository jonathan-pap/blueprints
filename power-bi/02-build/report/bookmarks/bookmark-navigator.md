# Bookmark navigator visual

Built-in visual that lists bookmarks as clickable buttons.

## CLI

```bash
pbir add visual bookmarkNavigator "<project>.Report/Overview.Page" \
  --x 24 --y 600 --width 600 --height 80
```

## Configure which bookmarks appear

By default lists all report bookmarks. To filter to a specific group:

```bash
pbir visuals set "<...>/BookmarkNavigator.Visual" --bookmark-group "Scenarios"
```

## Style

Inherits button styling from the theme. To override per-instance, see `../format/override-property.md`.

## After

`../validate/validate.md`.
