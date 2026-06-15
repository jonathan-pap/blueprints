# Archetype — Narrative Story

> **Audience:** a reader being walked through an argument. **Statement:** "Here's what happened." An
> author-driven, guided sequence — the report makes a case, page (or section) by section. Minimal
> slicers; the path is curated, not explored.

## Intent

- **Argument over exploration** — each section advances a point; charts are evidence for a stated
  takeaway, not an open canvas.
- **Caption-led** — every visual carries a one-line takeaway ([S4 caption annotations](../signatures.md#s4-caption-style-annotations-under-every-visual)). The caption is the headline; the chart proves it.
- Reading order is explicit (top→bottom, or paged). Generous whitespace, editorial pacing.
- Few or no slicers — a guided narrative shouldn't fork. Drillthrough for "want more" is fine.

## Zone allocation (3-30-300)

Narrative pages often invert the gradient — **prose/takeaway leads, chart supports**. Think in
*sections* (intro → evidence → evidence → conclusion) rather than strict KPI/analysis/detail bands.

| Section | Fills with | Notes |
|---|---|---|
| Lede | insight title + a framing sentence (textbox or smart-narrative measure) | sets the claim |
| Evidence blocks | one chart + its caption, repeated | each block = one point |
| Close | the conclusion / "so what" + a call to the next page | drillthrough to detail/appendix |

## Layout variants

| Variant | When (data signal) | Shape |
|---|---|---|
| **A — Vertical scroll-story** | a linear argument, one canvas | stacked chart+caption blocks, lede top, conclusion bottom |
| **B — Paged chapters** | distinct chapters / time periods | one point per page; bookmark/button navigation between |
| **C — Annotated hero** | one chart carries the whole story | a large annotated chart (callouts on the data) + supporting context |

## Chart mix
Line/area for time stories, annotated bar/column for comparisons, one annotated hero chart, textboxes
for prose. Annotations + captions do the talking. Use a [thin-report measure](../../calculations/thin-report-measure.md)
or smart narrative for dynamic takeaway text (verify formatting mechanics first).

## Density & tone
Low density (ratio 1.5–1.618), generous margins. Tones: **Editorial Newsroom**, **Scholarly Calm**,
**FT Pink Financial**. Signature: [S4 captions](../signatures.md#s4-caption-style-annotations-under-every-visual), [S2 display serif](../signatures.md#s2-display-serif-headlines), [S10 hairline rules](../signatures.md#s10-hairline-rules-instead-of-borders).

## Common failure
A dashboard pretending to be a story — lots of slicers, no takeaways, no order. If the reader has to
explore to find the point, it's an Analytical Canvas, not a Narrative.

## Job to be done
Primary user: board member / senior stakeholder / external audience. Trigger: a presenter making a case
("Revenue missed $42M. Three drivers. Here's the plan."). Mode: author-driven argument — reader is
convinced, not exploring. Success: reader restates the argument in one sentence. Failure: "so what?"
after viewing. Implication: minimal interactivity; content curated, not generated on the fly.

> **Story structure (Segel & Heer):** Martini-glass (linear → open exploration at the end) · interactive
> slideshow (linear steps + side trips) · drill-down story (hub + spoke detail pages). Pick by structure.

## Charts — use / don't-use
| Use | Don't use |
|---|---|
| annotated `lineChart`, slope (sim. line), `waterfallChart`, dumbbell (sim. bar), `textbox` prose, `shape` annotations | dense dashboards (>3 visuals), unannotated charts, matrix >2 measures, slicer-heavy layouts |

## Decision checklist
- [ ] every page title is a thesis sentence · [ ] one anchor chart per page, annotated · [ ] body text: shows → matters → so-what
- [ ] palette = highlight + grey (≤2 non-grey) · [ ] Prev/Next always visible · [ ] no slicers on narrative pages
- [ ] page `displayName` reads as a table of contents · [ ] reader can restate the argument after viewing

## Related
- [comparative-benchmark.md](comparative-benchmark.md) (evidence pages) · [analytical-canvas.md](analytical-canvas.md) (the appendix)
- [`../../bookmarks/bookmark-navigator.md`](../../bookmarks/bookmark-navigator.md) · [`../../add-visual/textbox.md`](../../add-visual/textbox.md)
