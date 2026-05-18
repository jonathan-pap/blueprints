# Brief structure: single file vs folder

## Single-file default

`projects/<name>/brief.md` — one structured file with the 8 sections from `brief-template.md`. Best for:

- Small / medium reports (< 5 pages, single audience)
- One author maintaining the brief
- Fast iteration

When in doubt, **default to single file.** Easier to read, easier to diff in PRs, harder to lose track of.

## Folder for bigger briefs

`projects/<name>/brief/` — split when:

- The brief grows past ~300 lines and individual sections need history
- Multiple stakeholders own different sections (KPIs owned by Finance, layout owned by Design)
- The brief evolves at different cadences (data sources stable, KPIs change quarterly)
- You want sub-files that link to other artifacts (e.g. `04-constraints.md` references a signed-off accessibility checklist)

## Recommended folder layout

```
projects/<name>/brief/
├── 00-context.md           ← audience, decision, cadence, consumption channel
├── 01-data-sources.md      ← model type, sources, refresh, volume, sensitivity
├── 02-kpis.md              ← measure list + target sources + formats
├── 03-pages-layout.md      ← page-by-page wireframe / decisions
├── 04-branding.md          ← theme, colors, logo, font
├── 05-constraints.md       ← perf SLA, accessibility, page size, non-goals
├── 06-open-questions.md    ← things to clarify; agent asks these first
└── 07-references.md        ← existing reports, source docs, sign-off threads
```

Numbered prefixes make the load order deterministic — the agent reads them alphabetically.

## When to split (and when not to)

| Signal | Split into folder? |
|---|---|
| Brief.md > 300 lines | Yes |
| Multiple owners maintaining different sections | Yes |
| KPI list will be edited frequently independent of layout | Yes |
| One stakeholder, < 5 pages, brief fits on one screen | No — keep single file |
| Brief barely fills 3 of the 8 template sections | No — single file is fine |

## Migration

Start single file. Split into a folder later if needed by:

```bash
cd projects/<name>
mkdir brief
# Split brief.md into 00-context.md, 01-kpis.md, etc.
# Original brief.md can be archived or kept as a navigation index
```

## Anti-pattern: split too early

Don't create a 7-file `brief/` folder for a 50-line brief. The overhead of navigating 7 mostly-empty files exceeds the value of organization. Start small, split when the file genuinely outgrows itself.

## What lives where (brief vs other docs)

- **`brief.md`** — what the report SHOULD do (intent, KPIs, layout decisions)
- **`README.md`** in the project — how to open / refresh / deploy
- **`outputs/*-audit.md`** — findings from `04-review/` runs (NOT in brief)
- **PR descriptions** — what changed in a specific commit (NOT in brief)

The brief is forward-looking ("what we want"). Audits, READMEs, and PR descriptions are point-in-time records.
