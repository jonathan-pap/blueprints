# Add a page filter

Filter that applies to every visual on the page.

## CLI

```bash
pbir filters add page "<project>.Report/Overview.Page" \
  --field "Date.Calendar Year" \
  --type Basic \
  --values "2026"
```

## Filter types

- `Basic` — discrete value list
- `Advanced` — expression-based (contains, starts-with, between)
- `TopN` — limit to top/bottom N
- `Relative` — last N days/months/years

## Locked vs hidden

```bash
pbir filters set "<...>" --locked   # user sees but cannot change
pbir filters set "<...>" --hidden   # user doesn't see it at all
```

## After

`../validate/validate.md`.
