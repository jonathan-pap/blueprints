# Add a culture / translation (TMDL)

One file per locale: `<project>.SemanticModel/definition/cultures/<locale>.tmdl`.

## Pattern

```tmdl
cultureInfo 'fr-FR'

    linguisticMetadata = {"Version": "1.0.0", "Language": "fr-FR"}
        contentType: json

    translation 'Sales' caption: 'Ventes'
    translation 'Sales' description: 'Faits de vente'
    translation 'Sales'.'Total Revenue' caption: 'Chiffre d''affaires total'
    translation 'Date'.'Year' caption: 'Année'
```

## Translation targets

- Table caption: `translation 'Table' caption: 'Localized Name'`
- Column caption: `translation 'Table'.'Column' caption: 'Localized Name'`
- Measure caption: `translation 'Table'.'Measure' caption: 'Localized Name'`
- Display folder: `translation 'Table'.'Column' displayFolder: 'Localized\Folder'`
- Descriptions: `translation 'Table' description: '...'`

Escape single quotes by doubling: `'Chiffre d''affaires'`.

## Linguistic metadata

The `linguisticMetadata` JSON powers Q&A natural-language queries in that locale. Can be empty `{"Version": "1.0.0"}` if you don't need Q&A.

## After

`bash ../../../04-review/hooks/validate-tmdl.sh "<project>.SemanticModel"`. Test by changing Desktop language or filtering for the locale.
