# Delete a page

Removes a page and every visual on it. There is no undo in PBIR — run the checks below first, because bookmarks, buttons and drillthrough targets that point at the page break silently.

```bash
pbir pages rm "<project>.Report/Page-Name.Page" -f
```

`-f` skips the confirmation prompt.

## Before deleting

Check if anything references the page:

```bash
grep -rn "Page-Name" "<project>.Report/"
```

Bookmarks and navigation visuals pointing at the page will break. Use `rename-page.md` if you really meant rename.

## After

`../validate/validate.md`.
