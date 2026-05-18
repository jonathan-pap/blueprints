# Add a table

Flat row list. For hierarchies, use `matrix.md`.

## Create

```bash
pbir add visual tableEx "<project>.Report/Overview.Page" --title "Order Details" \
  --x 24 --y 540 --width 1232 --height 196
```

## Bind fields

```bash
pbir visuals bind "<...>/Order Details.Visual" \
  -a "Values:Customers.Key Account Name" -t Column \
  -a "Values:Products.Product Name"      -t Column \
  -a "Values:Sales.Revenue"              -t Measure \
  -a "Values:Sales.Orders"               -t Measure
```

## Sort

Usually descending by the most important measure (often variance, not alphabetical):

```bash
pbir visuals sort "<...>/Order Details.Visual" -f "Sales.Revenue" -d Descending
```

## Format philosophy

Subtract, don't add. Remove gridlines, banding, default borders — let whitespace separate rows. Apply data bars to the primary measure and color scales to variance columns only.

## Templates

- `../examples/visuals/default/tableEx.json`
- `../examples/visuals/formatted/tableEx-gradient.json` — color-scale gradient on a measure column

## After

`../validate/validate.md`. Consider `../format/conditional-fmt-data-bar.md` for the magnitude column.
