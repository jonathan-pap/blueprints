# Add a visual-level filter

Filter scoped to one visual only. Use sparingly — page filters are usually cleaner.

## CLI

```bash
pbir filters add visual "<...>/Visual.Visual" \
  --field "Products.Category" \
  --type Basic \
  --values "Electronics,Furniture"
```

## When to use a visual filter

- This visual needs a different time window than the rest of the page
- This visual should exclude a known anomaly category
- Top-N filter ("top 10 customers by revenue")

## When NOT to use

- The filter should apply to multiple visuals → use a page filter (`add-page-filter.md`).

## After

`../validate/validate.md`.
