# Add a page

Don't add unless the report needs multiple pages. Most dashboards work as a single page.

## Create

```bash
pbir add page "<project>.Report/Details.Page" -n "Details"
```

**Always use the explicit page-path form** (`<project>.Report/<Page>.Page`). The shorthand `pbir add page "<project>.Report" -n "Details"` triggers a "thin reports require a connection" error even on thick projects.

The new page gets an auto-generated hash folder name (e.g. `4a96d1bd85ad3137`) and a `Title` textbox at (20, 20). The hash folder coexists with the display name `Details`.

> **Reference the page by its DISPLAY NAME, not the path label you passed.** The `<Page>` segment in
> the `add page` path is *not* the handle — `pbir add page ".../AllVisuals.Page" -n "All Visuals Test"`
> creates a hash folder whose display name is **"All Visuals Test"**, so later commands address it as
> `".../All Visuals Test.Page"` (or by the hash id), **not** `".../AllVisuals.Page"`. To get a clean,
> predictable handle, either pass a matching `-n`, or run `pbir pages rename … -p "{displayName}"` (below)
> so the folder name equals the display name.
>
> **Keep display names unique.** Two pages with the same display name make every later
> `pbir add visual` / `pbir rm` **ambiguous** (it lists all matches and fails). Since `add page` is
> **not atomic** — a failed run (e.g. the [schema-lag write block](../../../04-review/audit/pbir-validate.md#-the-lag-can-fatally-block-writes--not-just-colour-validate-output))
> can leave a partial/orphan page — verify with `pbir ls "<project>.Report"` after a failure and delete
> strays (`pbir rm "<...>/<Name>.Page" -f`) before retrying.

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
