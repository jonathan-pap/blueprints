# Conditional formatting — data bar

In-cell horizontal bar showing magnitude. Use on the primary measure column in tables.

## Apply

```bash
pbir visuals conditional-format "<...>/Visual.Visual" \
  --target "Sales.Revenue" \
  --type dataBar \
  --positive-color "#118DFF" \
  --negative-color "#D4602E"
```

## When to use

- Primary magnitude column in a `tableEx`
- Anywhere the reader needs to scan for "which row is biggest"

## When NOT to use

- Already using color scale on the same column
- More than 50 rows visible — bars become noise

## After

`../validate/validate.md`.
