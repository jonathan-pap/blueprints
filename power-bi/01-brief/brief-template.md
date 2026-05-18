# Brief template

Copy this file to `projects/<project-name>/brief.md` and fill in the bracketed sections. Delete sections that don't apply. The agent reads this BEFORE asking you questions.

For larger projects, split into a `projects/<project-name>/brief/` folder — see `brief-folder-structure.md`.

---

```markdown
# Brief — <Project Name>

Last updated: YYYY-MM-DD

## 1. Audience & decision

- **Primary audience:** [who reads this? executives / analysts / ops team / Copilot users / mixed]
- **Decision this report supports:** [one sentence — e.g., "weekly sales review", "monthly board pack", "real-time ops dashboard"]
- **Decision cadence:** [daily / weekly / monthly / on-demand]
- **Consumption channel:** [Power BI Service / mobile / embedded / printed PDF / Copilot Q&A]

## 2. Source data & model

- **Semantic model:** [thick PBIP / thin (connects to <Workspace>/<Model>.SemanticModel)]
- **Source systems:** [SAP / Salesforce / Snowflake / Excel / Fabric Lakehouse]
- **Refresh cadence:** [hourly / nightly / weekly / real-time via DirectQuery / Direct Lake]
- **Volume:** [rows in fact table; helps with capacity sizing]
- **Sensitive data:** [yes/no; sensitivity label required]

## 3. KPIs (2–5 max)

Per `references/kpi-selection.md`: apply the 20% change test.

| KPI | Measure name | Target source | Format |
|---|---|---|---|
| Revenue | `[Total Sales]` | Prior year (`[Sales 1YP]`) | $#,##0 |
| Margin | `[Profit %]` | Budget threshold (15%) | 0.0% |
| [...] | [...] | [...] | [...] |

If KPIs aren't known yet, list candidate metrics and the agent will help pick.

## 4. Pages & layout

| Page | Purpose | Key visuals | Layout pattern |
|---|---|---|---|
| Overview | Executive summary | KPI row + trend + breakdown + detail table | 3-30-300 |
| Trends | Time-series analysis | Line + combo + scatter | Stacked |
| Distribution | Part-to-whole | Donut + waterfall + matrix | 2-up + full-width |
| [...] | [...] | [...] | [...] |

Specify page count; agent will not invent extra pages.

## 5. Branding & style

- **Theme:** [sqlbi (default) / company-branded / specific JSON file path]
- **Primary brand colors:** [hex codes; agent prefers theme over per-visual hex]
- **Logo:** [path to image file if needed in header / corner]
- **Font:** [Segoe UI (default; safest) / custom (warn: doesn't ship to all consumers)]

## 6. Constraints & non-goals

- **Performance:** [sub-second visuals required? acceptable latency?]
- **Accessibility:** [WCAG AA / AAA / not required]
- **Page size:** [1280×720 standard / 1920×1080 high-res / custom]
- **Don't build:** [pages or features explicitly out of scope]
- **Deferred:** [things that will come in v2; don't waste time scoping them now]

## 7. Open questions

List anything you're not sure about. The agent will surface these as the first questions to clarify, rather than guessing.

- [ ] Should the Margin KPI use absolute variance or %?
- [ ] Is there an existing approved color palette?
- [ ] Does the ops team need a dedicated page or can they use a slicer?

## 8. References

- Existing reports to match: [list paths or links]
- Source data documentation: [links to wiki / catalog]
- Stakeholder sign-off thread: [link to ticket / email]
```

---

## After filling this in

1. Save to `projects/<name>/brief.md` (or split into `projects/<name>/brief/*.md`).
2. Tell Claude: "build the report" (or specific intent). The agent reads the brief, fills any gaps via `AskUserQuestion`, proposes a concrete layout, then enters `02-build/`.
3. Update the brief as the project evolves — it's the source of truth for "why does this report look like this".
