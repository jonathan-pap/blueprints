# Accessibility

> WCAG for Power BI reports — contrast, alt text, keyboard, colour-vision. **Read before finalizing
> any report.** Accessibility is not a polish step; it's a constraint that shapes colour, type, and
> layout from the start. The [validator](../../../04-review/audit/layout-contract-validate.md) and
> [anti-patterns.md](anti-patterns.md) enforce these; this file is the *why* and the *how*.

## Core principles

1. **Colour is never the sole signal** (WCAG 1.4.1) — always pair colour with shape, label, icon, or
   pattern. (Cross-check [signatures S8/S15](signatures.md), [color-palettes.md](color-palettes.md).)
2. **Contrast floors are non-negotiable** — 4.5:1 body text, 3:1 large text + non-text marks.
3. **Alt text describes the insight, not the chart type** — "Revenue rose 12% QoQ", not "a bar chart".
4. **Keyboard navigable** — every interactive element reachable without a mouse.
5. **Reading order matches visual hierarchy** — tab order follows the story, not creation order.
6. **≥24×24px interactive targets** — slicer items, buttons.
7. **Survives 200% zoom** — no clipping (cross-check [textbox height formula](signatures.md#s4-caption-style-annotations-under-every-visual)).

## WCAG 2.1/2.2 checklist for dashboards

| SC | Title | Dashboard implication | How to satisfy in PBI |
|---|---|---|---|
| 1.1.1 | Non-text Content | Every chart needs alt text | Set the visual's Alt text (static or DAX) |
| 1.3.1 | Info & Relationships | Grouping must be programmatic | Tab order + heading hierarchy, not just spatial proximity |
| 1.3.2 | Meaningful Sequence | Screen-reader order = visual layout | Set tab order in the Selection pane |
| 1.4.1 | Use of Colour | Colour not the only differentiator | Add label/icon/pattern alongside colour |
| 1.4.3 | Contrast (Min) | Body text ≥4.5:1 | Check every text/background pair |
| 1.4.11 | Non-text Contrast | Bars/lines/icons ≥3:1 | Verify data marks against canvas |
| 1.4.4 | Resize Text | Readable at 200% | Avoid fixed sizes that clip on zoom |
| 2.1.1 | Keyboard | All functions keyboard-operable | Test with Tab/Enter/Escape only |
| 2.4.3 | Focus Order | Focus sequence logical | Selection-pane tab order = reading order |
| 2.4.7 | Focus Visible | Focused element has indicator | Use PBI's default focus ring; don't override |
| 2.5.5 | Target Size | Targets ≥24×24px | Size slicer items, buttons, headers |
| 4.1.2 | Name, Role, Value | Interactive elements named | Visual titles + alt text |

## Contrast — formula + thresholds

```text
L = 0.2126·R + 0.7152·G + 0.0722·B        (relative luminance, linearized sRGB)
Ratio = (L_lighter + 0.05) / (L_darker + 0.05)
```

| Element | Min ratio | Level |
|---|---|---|
| Body text (<18pt reg / <14pt bold) | 4.5:1 | AA |
| Large text (≥18pt reg / ≥14pt bold) | 3.0:1 | AA |
| Non-text (icons, chart marks, borders) | 3.0:1 | AA |
| Enhanced body | 7.0:1 | AAA |

**Worked examples** (foreground on white `#FFFFFF`):

| FG | Ratio | AA body | AA large | AA non-text |
|---|---|---|---|---|
| `#333333` | 12.6:1 | ✅ | ✅ | ✅ |
| `#3182BD` | 4.6:1 | ✅ | ✅ | ✅ |
| `#767676` | 4.5:1 | ✅ | ✅ | ✅ |
| `#6BAED6` | 2.6:1 | ❌ | ❌ | ❌ |
| `#E15759` | 3.2:1 | ❌ | ✅ | ✅ |
| `#AAAAAA` | 2.3:1 | ❌ | ❌ | ❌ |

> Rule of thumb: mid-range hues on white usually **fail** body-text contrast. Test every pair —
> WebAIM Contrast Checker, or DevTools colour picker. Fix anything below 3:1 non-text / 4.5:1 body.

## Alt text — 4 reusable patterns

Lead with the insight, include real numbers, keep <150 chars for cards / <300 for complex visuals.

1. **Headline + Trend** — `"[Measure] [direction] [amount] over [period]. Now [value] vs [reference]."`
   → "Monthly revenue rose 12% over Q3. Now $4.2M vs $3.8M target."
2. **Structure + Finding** — `"[Chart] of [measure] by [dim]. [Finding]: [data point]."`
   → "Bar chart of sales by region. Western leads at $2.1M, 35% above the next."
3. **Comparison framing** — `"Comparing [measure] across [N] [items]. [Winner]: [v]. [Runner-up]: [v]."`
4. **Data-as-table fallback** — only for complex multi-measure visuals.

### DAX-driven alt text (filter-responsive)

When the insight changes with filters, bind alt text to a measure (a [thin-report measure](../calculations/thin-report-measure.md)):

```dax
Alt Text =
VAR _rev = FORMAT([Total Revenue], "$#,##0.0,,M")
VAR _chg = FORMAT([Revenue YoY %], "+0.0%;-0.0%")
VAR _per = SELECTEDVALUE('Date'[Quarter])
RETURN "Revenue is " & _rev & " in " & _per & ", " & _chg & " year over year."
```
Keep <300 chars after evaluation; state direction ("up"/"down"/"flat"); test across slicer states.

## Keyboard navigation reference

| Key | Action |
|---|---|
| `Tab` / `Shift+Tab` | Next / previous visual in tab order |
| `Enter` / `Space` | Activate / select |
| `Escape` | Exit / deselect |
| `Ctrl+Right/Left` | Move between data points in a visual |
| `Alt+Shift+F11` | Open filter pane · `Ctrl+F6` move between sections |

**Test protocol:** unplug the mouse; navigate the entire report with these keys. Every visual,
slicer, and button must be reachable and operable.

## Colour-vision deficiency (CVD)

- ~8% of males, ~0.5% of females. Most common: deuteranopia / protanopia (red-green), then tritanopia.
- **Safe palettes:** Okabe-Ito, Viridis, Cividis — all pass all three CVD types ([color-palettes.md](color-palettes.md)).
- **Simulate** before shipping: Chrome DevTools → Rendering → Emulate vision deficiencies.
- **Rule:** if any two palette colours become indistinguishable under simulation, add a second channel
  (label, shape, pattern).

## Power BI grounding

| Feature | Purpose | Configure |
|---|---|---|
| Alt text | Screen-reader description | Visual → General → Alt text (static or DAX) |
| Tab order | Keyboard sequence | View → Selection pane → drag into reading order |
| Show as table | Data fallback | On by default; keep enabled |
| Theme contrast | Global text/bg | Set `foreground`/`background` in theme ≥4.5:1 ([../../theme/create/color-system.md](../../theme/create/color-system.md)) |
| High-contrast mode | OS support | PBI respects Windows High Contrast; test it |

## Archetype a11y priorities

| Archetype | Priority concern | Why |
|---|---|---|
| Executive | Alt-text quality | Often read aloud / emailed — alt text IS the content |
| Operational | Keyboard + target size | Control rooms / kiosks; mouse may be absent |
| Analytical | Show-as-table | Power users need raw data; screen readers navigate tables |
| Narrative | Reading order | Story depends on sequence |
| Comparative | CVD-safe colour + non-text contrast | Colour carries the comparison signal |

## Testing checklist (before publish)

- [ ] Keyboard-only navigation reaches every visual/slicer/button
- [ ] Screen reader (NVDA/Narrator) announces alt text; reading order logical
- [ ] Zoom 200% — no clipping/overlap/truncation
- [ ] High-contrast mode — nothing invisible
- [ ] CVD simulation — all colour-coded info distinguishable
- [ ] Contrast ratios — body ≥4.5:1, large ≥3:1, non-text ≥3:1
- [ ] Tab order matches reading flow (Selection pane)
- [ ] Alt text on every non-decorative visual (insight-driven, not "chart")
- [ ] Touch targets ≥24×24px
- [ ] Data-table fallback renders on each visual

## Related
- [color-palettes.md](color-palettes.md) — CVD-safe palettes + contrast-aware assignment
- [anti-patterns.md](anti-patterns.md) — colour-misuse + low-contrast detection heuristics
- [`../references/visual-colors.md`](../references/visual-colors.md) — semantic colour + colourblind cues (build-time)
- [`../../../04-review/audit/layout-contract-validate.md`](../../../04-review/audit/layout-contract-validate.md) — the a11y gate
