# Create a bookmark

Snapshots current page state — selections, filters, visibility — into a named bookmark.

## CLI

```bash
pbir bookmarks new "<project>.Report" --name "Quarterly View" \
  --page "Overview.Page" \
  --capture-data --capture-display --capture-current-page
```

## Capture flags

- `--capture-data` — preserves filter and slicer values
- `--capture-display` — preserves visual visibility (spotlight, focus)
- `--capture-current-page` — navigation jumps to the captured page

Drop a flag to make the bookmark NOT touch that aspect (e.g., omit `--capture-current-page` for a reset-filters bookmark that stays on the current page).

## Personal vs report bookmarks

These are report-level (saved with the file). Personal bookmarks are user-level, created in Desktop / Service, and don't appear in the PBIP.

## After

`../validate/validate.md`. Test in Desktop to confirm the captured state restores correctly.
