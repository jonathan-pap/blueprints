# Cards & KPIs — build best-practices

> *Which* metrics to show is the brief-room decision ([../../../01-brief/references/kpi-selection.md](../../../01-brief/references/kpi-selection.md)).
> This file is *how* to build the card once the metric is locked. A bare number can't be judged;
> every KPI must answer two questions without thought: **"good or bad?"** (target + gap) and
> **"better or worse?"** (trend).

## The three elements

| Element | Purpose | Example |
|---|---|---|
| Actual value | magnitude | 518M |
| Target / comparison | the benchmark | Target: 483M |
| Gap (delta) | answers "good or bad?" | +35.4M (+7.3%) |

Show the gap in **both** absolute and % terms (absolute = scale, % = significance). Always
**label the target** — set `goals.goalText` to the comparison (`"1YP"`, `"Budget"`, `"3M Avg"`)
so the reader doesn't have to guess what they're comparing against.

## Build options

- **`kpi` visual** — built-in `Indicator` / `Goal` / `TrendLine` roles cover all three elements. → [../add-visual/kpi-card.md](../add-visual/kpi-card.md)
- **`card` visual + extension measures** — compute the gap text + color yourself. → [../add-visual/card.md](../add-visual/card.md)

```dax
-- gap as formatted text (reportExtensions.json or model)
Revenue vs Target =
VAR _gap = [Actuals MTD] - [Sales Target MTD]
RETURN FORMAT(_gap, "+#,##0;-#,##0") & " (" & FORMAT(DIVIDE(_gap,[Sales Target MTD]), "+0.0%;-0.0%") & ")"

-- gap color → theme sentiment token (not hex)
Revenue vs Target Color = IF([Actuals MTD] >= [Sales Target MTD], "good", "bad")
```

## Formatting with intent

**Size hierarchy:** headline number largest/boldest → gap medium/colored → target+trend smallest/muted.

**Color the gap, not the value.** Conditional-format the judgment indicator only. Pair color
with a directional arrow so the message survives colorblindness. Use accessible sentiment colors
in the theme (`good`/`bad`/`neutral`; blue/orange beats red/green). See [visual-colors.md](visual-colors.md).

### Display units — don't trust "Auto"

"Auto" display units break when a measure has a custom format string (the format string wins →
raw unrounded numbers). Query the value with active filters, then set units explicitly:

```text
value >= 1e12 → Trillions ; >= 1e9 → Billions ; >= 1e6 → Millions ; >= 1e3 → Thousands ; else None
precision: 1 digit before the unit → 1 ; 2+ digits → 0     (e.g. 3.8M→p1, 35bn→p0, 338K→p0)
percentages → unit None, precision 1 (format string carries the %)
```

KPI `indicatorDisplayUnits` enum: `0` Auto (avoid), `1` None, `1000`, `1000000`, `1000000000`, `1000000000000`. Set `indicator.indicatorDisplayUnits` + `indicator.indicatorPrecision` per visual.

### Title vs category label — show one, not both

A card shows the metric name in two places: the visual **title** and the **category/callout
label**. Showing both is redundant.
- **Category label only (preferred):** hide the visual title — the label reads "3.8M Order Lines" under the number, leaving room for a big value.
- **Title only:** set `categoryLabels.show=false` when the page title already gives context.

Hide auto-subtitles (`subtitle.show=false`) — they just repeat field names. Card min height
**130–150px** so value+label don't clip; raise height before shrinking font.

## Icons

Icons must be SVG extension measures with `dataCategory: ImageUrl` — see [../../visuals/svg/_index.md](../../visuals/svg/_index.md). Use sparingly, only when the icon adds information beyond color+number.

## Visual-type selection

| Scenario | Type |
|---|---|
| value + target + trend line | `kpi` |
| simple headline number | `card` + extension measures |
| several related metrics | `multiRowCard` |
| custom layout / sparkline / icons | `card` + SVG measure |

## Anti-patterns

| Anti-pattern | Fix |
|---|---|
| bare number, no target | add target + gap |
| > 5 cards | cut to the page's central question |
| loud color on the value | color the gap instead |
| 517,893,412 | round to 518M |
| title + category label both shown | show one |
| red/green only | pair with arrow/icon |
| relying on Auto units | query + set units explicitly |

## Review checklist

- [ ] Each card serves the page's central question; ≤ 5 cards
- [ ] Target/comparison present and labelled (`goalText`)
- [ ] Gap shown absolute + %
- [ ] Conditional color on the gap, paired with a secondary cue
- [ ] Rounded for summary level; consistent units across the page
- [ ] Subtitle hidden; one of title/category label only
- [ ] Font hierarchy value > gap > label > trend
