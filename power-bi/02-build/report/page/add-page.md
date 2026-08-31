# Add a page

**Rule: add a page only if the report spec asks for multiple pages.** Single-page dashboards are simpler and read better on most screens. Add a second page only if the brief explicitly requires it.

**Rule: page names must be unique and match their folder names.** The `pbir` CLI auto-generates hash folder names (e.g. `4a96d1bd85ad3137`) when you add a page, but you reference the page by its **display name** in later commands. Keep the display name and folder name synchronized (e.g., both "Guild Overview") so the page is predictable to reference and easy to find in the file tree. Mismatched or duplicate display names cause ambiguous references in later `pbir add visual` and `pbir rm` commands.

**Rule: each page gets a default title textbox.** When you create a page, it arrives with an auto-generated `Title` textbox at position (20, 20). Delete or replace it only if the brief specifies custom page titles or no title at all.

## Create a page

Use the explicit page-path form. The `<Page>` segment is a temporary label; the display name (passed via `-n`) is what you'll use later:

```bash
pbir add page "<project>.Report/Details.Page" -n "Guild Overview"
```

**Why the explicit form?** The shorthand `pbir add page "<project>.Report" -n "Details"` triggers a "thin reports require a connection" error even on thick PBIP projects.

After adding, verify the page exists with the correct name:

```bash
pbir ls "<project>.Report"
```

If the folder name doesn't match the display name, clean it up with `rename-page.md` so later references are predictable.

**Failure recovery:** The `add page` command is not atomic — a failed run (e.g., if the PBIR schema is locked) can leave a partial or orphaned page. Verify with `pbir ls` after any error, and delete strays with `pbir rm "<project>.Report/<Name>.Page" -f` before retrying.

## Customize the page title (optional)

The page arrives with a default `Title` textbox. If the brief specifies a custom title format (e.g., "Guild Overview — Rank Summary"), replace the auto-generated one:

```bash
pbir add title "<project>.Report/Guild Overview.Page" "Guild Overview — Rank Summary"
```

## Validate

After adding or modifying any page, run `../validate/validate.md` to catch schema errors.
