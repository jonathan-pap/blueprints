# Add a page title (textbox)

New Page 1 already has a title textbox at (20, 20). For new pages, add one explicitly for visual consistency.

## CLI

```bash
pbir add title "<project>.Report/Overview.Page" "Sales Overview" --x 24 --y 24
```

## Sizing

Default height: 56 px. Width: page width − (2 × margin), e.g. 1232 on a 1280-wide page with 24 margins.

## Title hierarchy

Don't repeat the same words at page-title → visual-title → subtitle levels:

- Page title: the **subject** (`"Revenue"`)
- Visual titles: the **differentiator** (`"by Region"`, `"Monthly Trend"`)
- Subtitles: usually hidden

## After

`../validate/validate.md`.
