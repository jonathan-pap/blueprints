# Fragment layout (after `serialize`)

```
<theme>_serialized/
├── meta.json              {name, version}
├── dataColors.json        ["#118DFF", ...]
├── textClasses.json       {callout, title, header, label, largeTitle}
├── sentiment.json         {good, bad, neutral, minColor, maxColor}
├── wildcard.json          visualStyles["*"]["*"]
└── visual-types/
    ├── lineChart.json
    ├── clusteredBarChart.json
    ├── clusteredColumnChart.json
    ├── cardVisual.json
    ├── kpi.json
    ├── tableEx.json
    ├── pivotTable.json
    ├── slicer.json
    ├── donutChart.json
    └── ...  (one file per visual type present in the theme)
```

## What lives where

- **Palette** → `dataColors.json` — the array `dataColors[]` from the monolith
- **Text styles** → `textClasses.json` — `textClasses` object
- **Sentiment / semantic** → `sentiment.json` — top-level sentiment color map (when present)
- **Global formatting defaults** → `wildcard.json` — `visualStyles["*"]["*"]`
- **Per-visual-type overrides** → `visual-types/<type>.json` — `visualStyles["<type>"]["*"]`

## What's NOT a fragment

The `name` and schema URL stay in `meta.json` — they're top-level monolith properties, not formatting.

## Editing rule

Touch only the fragment you mean to change. Don't edit `meta.json` (theme name) unless renaming. Don't edit multiple fragments in one commit unless they're logically related — small diffs make better reviews.
