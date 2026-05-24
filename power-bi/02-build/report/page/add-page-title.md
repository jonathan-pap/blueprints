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

## Three ways to render a title

| Option | When |
|---|---|
| **textbox** (default) | static page title — the standard choice |
| **shape with text** | styled background bar behind the title |
| **card visual** | **dynamic** title that includes a measure/filter value |

For a textbox, paragraphs carry the text + per-run style:

```json
"paragraphs": [
  { "textRuns": [
    { "value": "Sales ",    "textStyle": { "fontSize": "24pt" } },
    { "value": "Overview",  "textStyle": { "fontSize": "24pt", "fontWeight": "bold" } }
  ] }
]
```

Multiple paragraph objects stack as title + subtitle lines.

## Dynamic titles (filter-aware)

Drive a `card`/textbox from a measure to reflect the current filter context or refresh time:

```dax
Title Text = "Sales by Region — " & SELECTEDVALUE('Date'[Year], "All Years")
Refreshed  = "Updated: " & FORMAT(MAX('Refresh Log'[Timestamp]), "MMM dd, yyyy")
```

## Disable the chrome

A title visual should carry no container chrome — set `title`, `background`, `border`, and
`dropShadow` to `show=false`. Best done once in the theme so every page title inherits it:

```json
"visualStyles": { "textbox": { "*": {
  "title": [{ "show": false }], "background": [{ "show": false }],
  "border": [{ "show": false }], "dropShadow": [{ "show": false }]
} } }
```

See [../../theme/modify/visual-type-override.md](../../theme/modify/visual-type-override.md).

## Best practices

- Same x/y/size/font across **all** pages (consistency aids navigation + accessibility).
- Describe the page purpose; don't repeat the report name if it's obvious.
- Keep it readable at mobile width.

## After

`../validate/validate.md`.
