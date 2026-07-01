# Change text classes

Power BI exposes named text styles (`callout`, `title`, `label`, `header`) that visuals reference. Edit once in the theme, every visual updates.

## Quick CLI

```bash
pbir theme set-text-class "<project>.Report" callout \
  --font "Segoe UI Semibold" --size 24 --color "#252423"

pbir theme set-text-class "<project>.Report" title \
  --font "Segoe UI" --size 14 --color "#252423"
```

## Audit + swap fonts across the whole report (`pbir fonts`, 0.9.25)

`set-text-class` edits the theme; **`pbir fonts`** audits and rewrites fonts across the **report *and*
theme together** (visual properties, visual container, text classes, and `visualStyles`). Needs
**≥ 0.9.25**:

```bash
pbir fonts list "<project>.Report"                                   # audit: families, sizes, weights, styles (report + theme)
pbir fonts available                                                 # the built-in PBI font families (the safe set below)
pbir fonts replace "<project>.Report" --from "Calibri" --to "Segoe UI" -f   # brand swap a family everywhere
pbir fonts clear "<project>.Report" --size --weight -f               # drop per-visual size/bold overrides so the text-class wins
pbir fonts clear "<project>.Report" --all -f                         # clear family/size/weight/style/units/decimals/format
```

`fonts clear` is the enforcer for "edit once in the theme, every visual updates" — it removes the
per-visual overrides that would otherwise shadow the text class. `replace` (dry-run default) is the
brand/font-rule sweep.

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
