# AI / Copilot readiness checklist

Specifically for models consumed by Copilot or data agents. Skip this category for report-only consumption.

## Before investing

AI readiness can easily double model dev time. Confirm with the user:

1. **Will users actually use conversational BI?** If report-only, AI prep is low priority.
2. **Is the model stable enough?** AI prep is iterative; defer until structural churn stops.
3. **Is Copilot / data agent enabled in the tenant?** Check tenant settings first.

## The decision: reports / conversational BI / both?

| Consumption | Model design impact |
|---|---|
| Reports only | Standard: star schema, good measures, appropriate grain |
| Conversational BI | All of the above PLUS: AI instructions, AI schema, verified answers, linguistic schema, synonyms, English naming, descriptions optimized for AI |
| Both | Full investment in both |

## Section 1 — Model architecture (foundation)

- [ ] Star schema; no flat / denormalized / pivoted structures
- [ ] Correct data types on all columns
- [ ] Unnecessary columns and tables removed
- [ ] **Explicit DAX measures for all key metrics** (implicit measures are invisible to data agents)
- [ ] Report-scoped extension measures moved to the model (extension measures invisible to data agents)
- [ ] Duplicate / overlapping measures consolidated or clearly differentiated

## Section 2 — Naming and metadata

Highest-impact AI prep work — AI interprets field names literally.

- [ ] Human-readable names everywhere; no CamelCase, snake_case, UPPER_CASE, technical abbreviations (TR_AMT, CustName)
- [ ] Synonyms configured for alternative terminology (Revenue/Sales/Turnover for the same measure)
- [ ] Row labels set on dimension tables (helps AI find the "name" column)
- [ ] Default summarization set correctly on numeric columns (prevents accidental summing of IDs)

See `../../02-build/model/naming/` for the full naming work.

## Section 3 — Descriptions (AI vs human)

**Good descriptions for AI are different from good descriptions for humans.**

**For AI / agents:** disambiguate and direct.
> "When a user asks for Margin, they are referring to Standard Margin (this measure). Use this field, not Gross Margin or Contribution Margin."

**For human users:** explain calculation and source.
> "Standard margin = revenue minus standard cost of goods sold, using the valuated production cost from the manufacturing plant."

- [ ] Descriptions on all visible tables, columns, measures
- [ ] Descriptions add value beyond restating the field name
- [ ] AI-focused descriptions disambiguate + name preferred usage + describe relationships
- [ ] Human-focused descriptions explain calculation + source + business context
- [ ] If both audiences needed, use AI instructions for AI guidance, descriptions for humans

**Do not rely solely on AI to generate descriptions.** AI-generated ones tend to verbose-restate what's already inferable from structure. Always review with business knowledge.

## Section 4 — AI instructions

Freeform text Copilot + data agents read automatically. One of the highest-impact controls.

**Include:**
- Business terminology definitions with examples ("TMS = total media spend, calculated using `[total_media_spend]`")
- Time period definitions (fiscal year start, peak season, reporting cadence)
- Metric preferences ("when users ask about margin, use Standard Margin")
- Date field disambiguation ("Order Date is primary; Ship Date is only for logistics analysis")
- Default groupings and analysis preferences
- Example DAX queries for complex scenarios
- Instructions for Calculation Groups, DAX UDFs, or Field Parameters if present
- Visualization preferences for Copilot
- Output style (conciseness, question-asking behavior)

**Lives in:**
- `.md` file in `/Copilot` folder of a PBIP project (future location per Microsoft docs)
- Currently editable in Power BI Desktop ("Prep your data for AI"), VS Code, or Tabular Editor via C# macro
- **NOT automatically read by coding agents** (Claude Code, Codex, Copilot) — must be explicitly referenced

**Important:** AI instructions are a *writing* skill, not engineering. Inform from observing real Copilot interactions, not guessing. Iterate based on testing.

- [ ] AI instructions present and non-empty
- [ ] Business terminology documented
- [ ] Common question patterns addressed
- [ ] Refers to fields by their proper names
- [ ] Tested with Copilot or data agent
- [ ] Concise; non-contradictory with descriptions

## Section 5 — AI data schema

Controls which tables / columns / measures are visible to Copilot. Scoping correctly prevents confusion.

- [ ] Only relevant tables, columns, measures selected (not entire model)
- [ ] All dependent objects for selected measures included
- [ ] Helper / intermediate calc objects excluded
- [ ] Duplicate / overlapping measures excluded
- [ ] All fields required for verified answers are visible (not hidden)
- [ ] Schema selection matches between "Prep for AI" and data agent configuration

## Section 6 — Verified answers

Pre-built report visuals Copilot returns for specific questions.

**Note:** Often not worth the investment — Power BI visuals are poor for verified-answer rendering.

- [ ] Most common user questions identified (ask the user / team)
- [ ] Verified answers created with appropriate visuals
- [ ] Complete + robust trigger questions (not partial phrases)
- [ ] Both formal and conversational phrasings included
- [ ] Relevant filters configured per verified answer
- [ ] All fields used are visible in the model
- [ ] Trigger questions tested for exact and semantic matching

## Section 7 — Data agent configuration (if applicable)

- [ ] Same tables selected in data agent as in Prep for AI > AI Data Schema
- [ ] Model-specific instructions live in AI instructions, NOT at data agent level
- [ ] Data agent instructions limited to: response formatting, cross-source routing, common abbreviations, tone
- [ ] Routing instructions added if multiple data sources ("revenue questions → semantic model; real-time delivery → KQL database")
