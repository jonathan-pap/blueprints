# Theme brief template

Copy this file to `projects/themes/<theme-slug>/brief.md` and fill in the bracketed sections. Delete sections that don't apply. The agent reads this BEFORE asking discovery questions when you ask to author a theme.

---

```markdown
# Theme brief — <Theme Name>

Last updated: YYYY-MM-DD

## 1. Purpose & scope

- **Theme name:** [MyCorp Theme v1.0]
- **Why authoring:** [new brand rollout / replace inconsistent ad-hoc themes / accessibility refresh / dark variant of existing]
- **Reports it will apply to:** [single project / portfolio / all reports in <workspace>]
- **Distribution:** [Git source-of-truth / SharePoint / CLI template library / Fabric workspace]

## 2. Starting point

Per `starting-point.md`: never author from `{}`.

- **Base:** [sqlbi (bundled) / fluent2 / DataGoblins2021 / existing theme JSON path / extract from report <path>]
- **What to keep:** [palette only / typography only / wildcard only / everything as-is]
- **What to override:** [list sections you intend to change]

## 3. Color system (4 layers)

Per `color-system.md`. Fill what's decided; leave others for the agent to propose.

### Layer 1 — `dataColors` (series palette, ordered by frequency)
- [#1971c2, #f08c00, #2f9e44, ...] (6–12 colors, primary first)
- **Constraints:** [colorblind-safe / muted only / corporate hex list / WCAG AA]

### Layer 2 — Semantic (`good` / `bad` / `neutral`)
- good: [#2f9e44]
- bad: [#e03131]
- neutral: [#868e96]

### Layer 3 — Background / foreground variants
- foreground: [#343a40]
- background: [#ffffff]
- (light/dark/neutral variants if needed)

### Layer 4 — Accents (`tableAccent`, `hyperlink`, `shapeStroke`)
- [hex or "match dataColors[0]"]

## 4. Typography (`textClasses`)

Per `typography-roles.md`. Stick to Segoe UI / Segoe UI Semibold unless the user has a documented reason for a custom font.

| Role | Font | Size | Color |
|---|---|---|---|
| title | Segoe UI Semibold | 14 | #343a40 |
| header | Segoe UI Semibold | 12 | #343a40 |
| label | Segoe UI | 11 | #495057 |
| callout | Segoe UI | 32 | #343a40 |
| dataTitle | Segoe UI | 12 | #868e96 |

## 5. Wildcard defaults

Per `wildcard-defaults.md`. Confirm or override the standard set:

- **Title:** show by default? [yes/no]
- **Background:** [transparent / white / theme bg]
- **Border:** [none / 1px #dee2e6]
- **Drop shadow:** [off globally — recommended]
- **Padding:** [8px all sides]

## 6. Visual-type overrides

Per `visual-type-priorities.md`. Critical (must override): `textbox`, `image`, `shape`, `actionButton`.

Optional overrides:
- **kpi:** [indicator size / trend visibility / goal formatting]
- **card:** [category font / value size]
- **slicer:** [item font / header style]
- **lineChart:** [legend position / gridlines]
- **tableEx:** [column header bg / row alt color]

## 7. Constraints & non-goals

- **Accessibility:** [WCAG AA contrast on text/bg / not required]
- **Branding lock:** [hex codes are immutable / negotiable]
- **Don't include:** [things explicitly out of scope — e.g., no dark variant in v1]
- **Schema version:** [`reportThemeSchema-2.152.json` or latest]

## 8. Open questions

List anything you're unsure about. The agent will raise these first instead of guessing.

- [ ] Are corporate fonts approved for Power BI? (note: Power BI only supports its built-in font list)
- [ ] Is the green / red good-bad pair colorblind-safe enough?
- [ ] Should hyperlink color match `dataColors[0]` or be a distinct accent?

## 9. References

- Source brand guidelines: [link / file path]
- Existing theme JSON: [path if iterating]
- Reference reports to match: [paths]
- Designer / stakeholder sign-off: [link to thread / ticket]
```

---

## After filling this in

1. Save to `projects/themes/<theme-slug>/brief.md`.
2. Tell Claude: "build the theme" (or "create a theme"). The agent reads the brief, fills any gaps via `AskUserQuestion`, then walks the 7-step workflow in `_index.md`.
3. Update the brief as you iterate — it's the source of truth for "why does this theme look this way".

## See also

- `_index.md` — the 7-step authoring workflow
- `../../../projects/themes/README.md` — where the theme JSON + brief live on disk
- `../../../01-brief/brief-template.md` — equivalent template for report projects
