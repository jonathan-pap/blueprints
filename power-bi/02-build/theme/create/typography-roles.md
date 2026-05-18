# Typography (`textClasses`)

Text classes define font properties by semantic role. Every defined class overrides Power BI's defaults for that role across all visuals.

## Standard roles

| Role | Typical use | Recommended size |
|---|---|---|
| `title` | Visual titles, page titles | 14–16pt |
| `header` | Section headers, column headers | 12–14pt |
| `label` | Axis labels, data labels | 11–12pt |
| `callout` | KPI values, prominent numbers | 28–36pt |
| `dataTitle` | KPI subtitles / labels | 12pt |
| `boldLabel` | Emphasized labels | 12pt |
| `largeTitle` | Large section titles | 20–24pt |
| `largeLabel` | Larger variant of label | 13–14pt |

## Font choice

- **`"Segoe UI"` for regular**, **`"Segoe UI Semibold"` for emphasis** — short name form only.
- In `visualStyles` and `textClasses`: short name. The long CSS font stack format (`"'Segoe UI Semibold', wf_segoe-ui_semibold, ..."`) is for `outspacePane` / `filterCard` only.
- **Do not use custom fonts** — Power BI only supports its built-in font list. Supported: Arial, Calibri, Candara, Consolas, Courier New, DIN, DIN Light, Georgia, Segoe UI, Segoe UI Light, Segoe UI Semibold, Segoe UI Bold, Tahoma, Times New Roman, Trebuchet MS, Verdana.
- **Mixing more than two font weights in a report creates visual noise.**

## Example `textClasses` block

```json
"textClasses": {
  "callout": {
    "fontSize": 32,
    "fontFace": "Segoe UI",
    "color": "#343a40"
  },
  "title": {
    "fontSize": 14,
    "fontFace": "Segoe UI Semibold",
    "color": "#343a40"
  },
  "header": {
    "fontSize": 12,
    "fontFace": "Segoe UI Semibold",
    "color": "#343a40"
  },
  "label": {
    "fontSize": 11,
    "fontFace": "Segoe UI",
    "color": "#495057"
  },
  "dataTitle": {
    "fontSize": 12,
    "fontFace": "Segoe UI",
    "color": "#868e96"
  }
}
```

## Critical gotcha — color format differs from visualStyles

`textClasses` colors use a **plain hex string** (`"color": "#343a40"`), NOT the `{"solid":{"color":"..."}}` object wrapper.

The nested wrapper is correct in `visualStyles` but WRONG in `textClasses` — using it causes the color to be **silently ignored**.

## After

Set wildcard container defaults next → `wildcard-defaults.md`. The wildcard references the text classes you just defined (e.g., `title.fontFamily` references `textClasses.title.fontFace`).

## See also

- `../modify/text-classes.md` — CLI to set text classes after theme exists
