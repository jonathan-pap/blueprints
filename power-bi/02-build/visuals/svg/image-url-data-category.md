# Set `dataCategory = ImageUrl`

Required. Without it, Power BI renders the measure's return value as raw text instead of an image.

## Set on the measure (TMDL)

```tmdl
measure 'Sparkline' = "data:image/svg+xml;utf8,<svg ...>...</svg>"
    dataCategory: ImageUrl
    lineageTag: <guid>
```

## Set via TOM (PowerShell, live)

```powershell
$m = $model.Tables["_Measures"].Measures["Sparkline"]
$m.DataCategory = "ImageUrl"
$model.SaveChanges()
```

## Set via Power BI Desktop UI

Select the measure → Column tools → Data category → Image URL.

## Verify

After setting, the measure shows a small image icon next to its name in the field list.

## Common mistake

Setting `dataCategory = WebUrl` instead of `ImageUrl`. Both render as clickable links; only `ImageUrl` renders the SVG inline.
