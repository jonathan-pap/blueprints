# Add a textbox

Use for page titles and captions. New reports already include a Page 1 title textbox at (20, 20) — rename rather than add a duplicate.

## Create (page title)

```bash
pbir add title "<project>.Report/Overview.Page" "Sales Overview" --x 24 --y 24
```

## Create (subtitle / caption)

```bash
pbir add subtitle "<project>.Report/Overview.Page" "Q4 2026 Performance"
```

## Custom textbox

```bash
pbir add visual textbox "<project>.Report/Overview.Page" \
  --x 24 --y 16 --width 1232 --height 56
```

Then edit the textbox content via the visual.json `paragraphs` array — see `../pbip-format/_index.md` for JSON structure.

## Title hierarchy rule

Don't repeat the same words across page title → visual title → subtitle. Distribute meaning:

- Page title: the subject (`"Revenue"`)
- Visual titles: the differentiator (`"by Region"`, `"Monthly Trend"`)
- Subtitles: usually hidden

## Templates

- `../examples/visuals/default/textbox.json`
- `../examples/visuals/formatted/textbox.json`

## After

`../validate/validate.md`.
