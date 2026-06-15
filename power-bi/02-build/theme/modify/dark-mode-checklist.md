# Dark-mode / re-theming checklist

> Switching an existing report's theme — especially **light↔dark** — is not just editing the theme
> JSON. Per-visual colour overrides sit **above** the theme in the cascade, so a theme edit alone
> leaves them stale. This is the consolidated sweep. For the redesign *workflow* that wraps it, see
> [`../../report/references/brownfield.md`](../../report/references/brownfield.md); to find the overrides,
> [`../audit/find-hardcoded-hex.md`](../audit/find-hardcoded-hex.md) + [`../audit/find-overrides.md`](../audit/find-overrides.md).

## Polarity-change gate (read first)

A dark↔light flip inverts foreground **text** colours that are hardcoded as `Literal` on shapes,
textboxes, slicers, cards, and nav buttons. **The theme does NOT override these** — omit them and the
text goes invisible. Sample mappings:

| | Dark text | Light text |
|---|---|---|
| Foreground | `#1F2937` / `#252423` / `#333333` | `#F9FAFB` / `#E6EDF3` / `#FFFFFF` |

> **"One explicit property poisons the group"** — if an `objects` group has even one explicit prop
> (e.g. `columnAdjustment: 'growToFit'`), *all* colour props in that group stop inheriting from the
> theme. You must set the colours explicitly for the whole group.

## Map by semantic role, not 1:1

Colours don't map across polarities by index. Map by what the colour *does*:
- Coloured header/accent bars (dark) → **white/transparent** (light)
- Dark card fills → `#FFFFFF` (the card surface — **not** the page-canvas background colour)
- Bright borders → soft/muted borders

### The `#FFFFFF` dual-meaning trap (light→dark)

`#FFFFFF` means two different things: a **card/surface fill** (→ swap to the dark card colour) and
**contrast text** on coloured bars (→ keep white). A blind hex sweep breaks one or the other. Exclude
`#FFFFFF` from the bulk sweep; replace it *only* inside `visualContainerObjects.background.color`, and
**leave** it in text contexts (`objects.text.fontColor`, textbox `textRuns` colour, title `fontColor`
on coloured bars).

## The 8-step sweep

1. **Structural colours together** — `firstLevelElements`/`foreground` + `background` +
   `secondaryBackground` in one pass. Setting only `background` → invisible text.
2. **`page.json` `objects.background.color` on EVERY page.** Pages with no `objects.background` default
   to white (a system default, not the theme `background`) — the sweep can't fix what isn't there; add
   it explicitly per page.
3. **Filter pane** — set `outspacePane` + `filterCard` (`Applied`/`Available`, PascalCase). The filter
   pane does **not** inherit structural colours → [`../../report/filters/configure-filter-pane.md`](../../report/filters/configure-filter-pane.md).
4. **All slicer types** — style `slicer`, `listSlicer`, `advancedSlicerVisual` in `visualStyles`; the
   legacy `"slicer"` key has **no effect** on modern slicers. Slicer `header.background` needs a
   *semantic* map (dark→light → `#FFFFFF`, not the new accent).
5. **Azure Map** — `mapControls.defaultStyle` is an **enum** (`night`/`grayscale_dark`/`high_contrast_dark`
   for dark; `road`/`grayscale_light` for light). A hex sweep never touches it — set it explicitly.
6. **`stylePreset: 'None'` on every `tableEx`/`pivotTable` with custom colours.** Style presets
   override `objects`-level `backColorPrimary/Secondary` — the single most common dark-mode table bug
   (silent: white rows, no error). → [`../../report/add-visual/table.md`](../../report/add-visual/table.md).
7. **Visual-specific dark props** — `tableEx`/`pivotTable` cell colours (`objects.values`,
   `columnHeaders`, not just VCO), card fills, shape fills, textbox runs.
8. **Contrast audit** — re-validate every text/background pair to WCAG AA after the swap
   ([`../../report/references/accessibility.md`](../../report/references/accessibility.md#contrast--formula--thresholds)).

## Sweep atomically

Update the theme JSON **and** bulk-sweep the inline `definition/` hex in **one step**, *then* reload
Desktop — don't reload mid-sweep. Theme JSON is cached by filename, so also rotate the theme file's GUID
suffix on any edit ([`../serialize/build.md`](../serialize/build.md), [where-themes-live](../where-themes-live.md)).

## Symptom → cause → fix

| Symptom | Cause | Fix |
|---|---|---|
| Table cells still white | `stylePreset` overrides `objects` colours | set `stylePreset: 'None'` (step 6) |
| Page still white | no `objects.background` on that page | add it explicitly (step 2) |
| Accent shape kept old colour | hardcoded `Literal` fill | sweep the shape `fill` |
| Slicer dropdown white | modern slicer + legacy key | style `advancedSlicerVisual`/`listSlicer` (step 4) |
| Invisible card/axis/title text | foreground `Literal` not swept | add explicit `fontColor` (steps 1, 7) |
| Shape text vanished | shape `text` has no `fontColor` to replace | **add** the property — a hex sweep can't fix a missing one |

## Preventive authoring (so future swaps are cheap)

Use `ThemeDataColor` for VCO `background`/`border`/`title.fontColor`, table `values.backColorPrimary`,
and `columnHeaders` — they then follow the theme. Use `Literal` hex only where `ThemeDataColor` breaks:
`dataPoint.fill` + metadata selector, and FillRule gradient stops
([`../../report/format/conditional-fmt-color-scale.md`](../../report/format/conditional-fmt-color-scale.md)).

## Related
- [`../audit/find-hardcoded-hex.md`](../audit/find-hardcoded-hex.md) · [`../audit/find-overrides.md`](../audit/find-overrides.md) · [`../promote/clear-visual-overrides.md`](../promote/clear-visual-overrides.md)
- [`../../report/references/brownfield.md`](../../report/references/brownfield.md) — the redesign workflow this fits into · [wildcard.md](wildcard.md) — wildcard padding/background caveats
