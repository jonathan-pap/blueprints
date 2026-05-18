# Culture (translations) — CRUD

A culture maps the model's invariant names to localized labels.

## Create

```powershell
$ci = New-Object Microsoft.AnalysisServices.Tabular.Culture
$ci.Name = "fr-FR"
$model.Cultures.Add($ci)

$lm = New-Object Microsoft.AnalysisServices.Tabular.LinguisticMetadata
$lm.Content = "{ ""Version"": ""1.0.0"" }"   # JSON blob; can be empty
$ci.LinguisticMetadata = $lm

# Translate a measure caption
$tr = New-Object Microsoft.AnalysisServices.Tabular.ObjectTranslation
$tr.Object   = $model.Tables["Sales"].Measures["Total Revenue"]
$tr.Property = [Microsoft.AnalysisServices.Tabular.TranslatedProperty]::Caption
$tr.Value    = "Chiffre d'affaires total"
$ci.ObjectTranslations.Add($tr)

$model.SaveChanges()
```

## Read

```powershell
$model.Cultures["fr-FR"].ObjectTranslations |
  ForEach-Object { "$($_.Object): $($_.Value)" }
```

## Update

```powershell
$tr = $model.Cultures["fr-FR"].ObjectTranslations |
  Where-Object { $_.Object.Name -eq "Total Revenue" }
$tr.Value = "CA Total"
$model.SaveChanges()
```

## Delete

```powershell
$model.Cultures.Remove($model.Cultures["fr-FR"])
$model.SaveChanges()
```

## TranslatedProperty enum

`Caption`, `Description`, `DisplayFolder`.
