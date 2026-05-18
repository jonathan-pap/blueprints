# Change text classes

Power BI exposes named text styles (`callout`, `title`, `label`, `header`) that visuals reference. Edit once in the theme, every visual updates.

## Quick CLI

```bash
pbir theme set-text-class "<project>.Report" callout \
  --font "Segoe UI Semibold" --size 24 --color "#252423"

pbir theme set-text-class "<project>.Report" title \
  --font "Segoe UI" --size 14 --color "#252423"
```

## All classes

- `callout` — KPI / card primary values (largest)
- `title` — visual titles
- `header` — table / matrix column headers
- `label` — axis labels, data labels
- `largeTitle` — page-title textboxes

## Font rule

Stick to `Segoe UI` and `Segoe UI Semibold`. Custom fonts aren't guaranteed to render on all consumer machines.

## Per visual-type override

If only `lineChart` titles need to be larger (not all titles), don't change the global text class — override the lineChart visual type. See `visual-type-override.md`.

## Verify

```bash
pbir theme text-classes "<project>.Report"
```

## After

`../../report/validate/validate.md`. Reopen Desktop.
