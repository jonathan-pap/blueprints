# Delete a page

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
