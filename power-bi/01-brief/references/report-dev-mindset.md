# Report-development mindset

> Stance to adopt before building anything. A report is a tool for a specific business problem,
> not a canvas. Most rebuilds trace back to skipping the questions below.

## Understand the problem first

Build a clear answer to each before touching the report (use `AskUserQuestion` until they're clear):

- **Who uses this?** Role, decisions they make, how often they look. A warehouse manager checking daily OTD needs a different report than a CFO reviewing quarterly.
- **What specific problem does it solve?** Not "show sales" but "identify which accounts are behind target so regional managers can intervene." A report that answers everything answers nothing.
- **What action follows a look?** No action → the report is decoration. Every visual should improve the reader's ability to act.
- **What does the reader already know?** Domain knowledge and meeting cadence decide what to show vs. omit.

A report built on assumptions gets rebuilt from scratch.

## Reports are problem-focused, not narrative

Reports don't tell stories — the user tells the story through interaction (cross-filter, drill,
slice). The report's job is to focus tightly on one problem and make it easy to explore.

- Every visual earns its place by answering a question tied to the problem; the rest is noise.
- Layout follows the detail gradient — summary up top, detail at the bottom ([../../02-build/report/layout/detail-gradient.md](../../02-build/report/layout/detail-gradient.md)).

## The report is only as good as the model

If the model lacks targets, time intelligence, clean hierarchies, or relationships, no amount of
formatting saves the report. Flag model gaps early instead of papering over them with report-level
hacks:

- No target/budget measures → raise it before building KPI cards.
- Missing time intelligence / incomplete date table → raise it.
- Ambiguous field names / missing descriptions → the report inherits the confusion.

When the model is the bottleneck, say so. Add the missing measures in the model room
([../../02-build/model/add/measure.md](../../02-build/model/add/measure.md)); use report-local extension measures only when the need is genuinely
report-specific ([../../02-build/report/calculations/thin-report-measure.md](../../02-build/report/calculations/thin-report-measure.md)).

## Formatting nothing means formatting everything

Formatting directs attention; it doesn't decorate. If every column is conditionally formatted,
nothing stands out. Apply with intent:

- Conditional formatting on variance/gap columns only.
- Color to encode meaning (good/bad/neutral), not to "pop."
- Data bars on the primary measure, not every number.
- The absence of formatting is itself a signal.

## Iteration is the process

Reports aren't one-shot. Set this expectation explicitly:

1. Interview — problem, audience, data.
2. Wireframe — propose a layout, get approval before building.
3. First draft — structure, bindings, basic formatting.
4. Review — render, validate ([../../04-review/context.md](../../04-review/context.md)).
5. Refine — adjust on feedback; repeat.

Push back on "finished report from one vague prompt" — that's not how effective development works.

## Think broader than Power BI

When the user complains, check the whole stack: is it the report, the model, the ETL, the data,
or the business process? Is Power BI even the right tool, or would Analyze-in-Excel, a Fabric
notebook, or a plain email serve better? Be willing to zoom out.

## Stance

- Be direct; push back on requests that collide with reporting/dataviz best practice. Flag when the problem, users, or requirements aren't well understood.
- Don't call anything "production-ready," "beautiful," or "perfect" — those are the reader's call, measured by actual use. If asked for a "good report," redirect to: are people using it? Has anyone checked usage metrics ([../../04-review/usage/report-detail.md](../../04-review/usage/report-detail.md))?
- Depth over speed; a poor result is worse than no result. Think *with* the user — propose alternatives, flag trade-offs, challenge assumptions.

## Related

- [vague-prompts.md](vague-prompts.md) — turning a thin prompt into a brief
- [kpi-selection.md](kpi-selection.md) — choosing the metrics
- [limitations.md](limitations.md) — what PBIR/this workflow can't do
