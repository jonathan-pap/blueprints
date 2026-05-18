# Rename a page

Preferred over delete + add — preserves bookmarks, navigation links, and any cross-page filters. Also renames the page folder so it matches the display name (cleaner than the auto-generated hash folder).

## CLI

```bash
pbir pages rename "<project>.Report/Page 1.Page" --to "Overview" -f
```

- `--to <Name>` — new folder + display name
- `-f` — execute (default is dry-run; without it nothing changes)

The folder is renamed AND `definition.pbir` updated. Bookmarks and links that target the page are updated too.

## Batch rename (apply pattern to every page)

```bash
pbir pages rename "<project>.Report" -p "{displayName}" -f
```

Renames every page folder to match its `displayName`. Useful after `pbir add page` creates pages with hash folder names (the auto-generated convention) and you want friendly folder names across the whole report.

Pattern tokens: `{displayName}`, `{name}`, `{index}`.

## Default Page 1

New reports ship with `Page 1`. Rename it to your real first-page name rather than adding a new one.

## After

`../validate/validate.md`. Reopen Desktop to confirm bookmarks still navigate correctly.
