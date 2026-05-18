# Add a page

Don't add unless the report needs multiple pages. Most dashboards work as a single page.

## Create

```bash
pbir add page "<project>.Report/Details.Page" -n "Details"
```

**Always use the explicit page-path form** (`<project>.Report/<Page>.Page`). The shorthand `pbir add page "<project>.Report" -n "Details"` triggers a "thin reports require a connection" error even on thick projects.

The new page gets an auto-generated hash folder name (e.g. `4a96d1bd85ad3137`) and a `Title` textbox at (20, 20). The hash folder coexists with the display name `Details`.

## Get clean folder names instead of hashes

After adding pages, rename them to use the display name as the folder name:

```bash
pbir pages rename "<project>.Report" -p "{displayName}" -f
```

See `rename-page.md`.

## Custom title afterwards (only if you want to replace the auto title)

```bash
pbir add title "<project>.Report/Details.Page" "Details"
```

## After

`../validate/validate.md`.
