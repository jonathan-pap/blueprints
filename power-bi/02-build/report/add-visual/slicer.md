# Add a slicer

Use for page-level filtering exposed as a visual. Limit to **3 slicers per page** — extras belong in the filter pane (`../filters/configure-filter-pane.md`).

## Pick the type first

Default to `slicer` (classic dropdown) unless the brief says otherwise.

| Field shape | Use |
|---|---|
| Single-select or few discrete values (Year, Region) | `slicer` (dropdown) — the default |
| Long discrete list the user scans/multi-selects | `slicer` in list mode, or `listSlicer` |
| Modern button/tile style, explicit multi-select | `advancedSlicerVisual` |

Mixing types across a report is a common inconsistency — pick one and pin it in `design-system.yaml` (`defaults.slicer.type`).

## Create

Use the size from the project's `design-system.yaml` (`defaults.slicer.size`) — default `240 × 40`:

```bash
pbir add visual slicer "<project>.Report/Overview.Page" --title "Year" \
  --x 24 --y 24 --width 240 --height 40
```

## Bind field

```bash
pbir visuals bind "<...>/Year.Visual" \
  -a "Values:Date.Calendar Year" -t Column
```

## Variants

- `slicer` — classic dropdown / list
- `advancedSlicerVisual` — newer button-style with multi-select

## Position consistently

All slicers on a page should sit in a single row at the top **or** a single column on the left. Pick one and stick to it across pages.

## Sync slicers across pages

When the same dimension filters more than one page (comparison reports especially), **sync** the
slicers so a selection carries across — otherwise each page has independent state and the comparison
silently lies. In PBIR this is a `syncGroup` (sibling of `visualType`):

```bash
pbir visuals sync-group "<...>/Year.Visual" --group "period" --filter --field
```

Rules:
- Same `groupName` across pages; members must share the **same `visualType`** and the same bound column.
- `--filter` syncs the applied filter; `--field` keeps the field binding in lock-step.
- A comparative report with independent slicer state is an [anti-pattern](../references/anti-patterns.md#cluster-6--archetype-mismatch).

> The `syncGroup` property is absent from some published PBIR schemas but Desktop reads/writes it
> correctly — `pbir validate` may warn cosmetically; confirm in Desktop.

## Temporal slicers — pick by grain, not by the date column existing

A date column does **not** mean a full-date `Between` picker. Match the control to the page question:
executive/annual pages → a **Year dropdown or tile**; arbitrary day/month range exploration → `Between`
(only when the field renders as a Date/DateTime). See [design/identity-workflow.md gotchas](../build-report.md#gotchas-check-each-before-handoff).

## Templates

- `../examples/visuals/default/slicer-list.json` — classic list slicer
- `../examples/visuals/default/slicer-dropdown.json` — dropdown mode
- `../examples/visuals/default/advancedSlicer.json` — newer button-style
- `../examples/visuals/formatted/slicer.json` — formatted list slicer
- `../examples/visuals/formatted/slicer-flash.json` — highlighted-selection variant
- `../examples/visuals/formatted/advancedSlicer-buttons.json` — button slicer with custom selection colors

## After

`../validate/validate.md`.
