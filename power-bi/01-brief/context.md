# Room 01 — Brief

> Discovery only. No edits to PBIP files in this room. The goal is to lock requirements before you enter `02-build/`.

## Pipeline (file-first, chat-second)

```
Check for brief.md → Read it → AskUserQuestion for gaps only → Propose → Lock
```

The agent's first action is **not** to ask questions — it's to look for a brief file. Chat-based discovery is only the fallback when no brief exists.

## Step 1 — Check for a project brief

Per `read-project-brief.md`:

1. Look for `projects/<name>/brief/` folder → read every `*.md` in alphabetical order
2. Otherwise look for `projects/<name>/brief.md` → read it
3. Otherwise no brief → fall through to chat-based discovery (Step 2 below)

If a brief exists and is comprehensive, skip Step 2 entirely. Go straight to Step 3 (Propose).

## Step 2 — Chat-based discovery (only when no brief / brief has gaps)

Per `references/vague-prompts.md`. Max 3 questions:

1. What decision does this report support?
2. Which 2–3 measures matter most? (If user can't name them, propose `pbir model "...Report" -d` to discover.)
3. Any style/brand preferences? (Default: sqlbi theme.)

If a brief exists but has `[fill in]` markers or "Open questions" — only ask about those. Don't re-ask things already answered in the file.

## Step 3 — Propose

Present a concrete layout proposal — KPI names, chart types, dimensions, filters, theme. Specific enough that the user can say "yes" or "change X".

## Step 4 — Lock

Once confirmed, route to `../02-build/context.md`.

Optionally write the locked decisions back to the brief — append to `brief.md`'s "Locked decisions YYYY-MM-DD" section, or create `brief/00-locked-decisions.md`. Keeps the brief as a living source of truth.

## When to enter this room

User says any of: "make me a dashboard", "build a report", "I want KPIs", "create something with..." — anything without an existing brief or explicit measure / audience / layout context.

Also enter when: user starts a new project (`projects/<new-name>/`) and there's no brief yet — point them at `brief-template.md`.

## When to exit

When you have:

1. Named **audience** and **decision** the report supports
2. **2–5 measures** identified (by name, from the model)
3. A **layout choice** (executive dashboard / operational / detail / custom)
4. A **theme decision** (default sqlbi or explicit override)

Then route to `../02-build/context.md`.

## Defaults (when brief silent + user deflects)

Apply silently; flag the result as a starting point.

- **Theme** — sqlbi (already bundled in new reports)
- **Layout** — Executive dashboard (KPI row → trend → breakdown → detail table)
- **Page size** — 1280 × 720
- **KPI count** — 3 cards, top
- **Time grain** — Match filter context (yearly → monthly; monthly → daily)
- **Conditional formatting** — Gap/variance only, semantic colors (`good`/`bad`)

## Rules

- **File-first.** Always check for `projects/<name>/brief.md` (or `brief/`) BEFORE asking questions.
- **Three questions max** (chat fallback). A 10-question intake kills momentum.
- **Never refuse a vague prompt.** Vague is normal. Close the gap with proposals.
- **Don't build here.** No `pbir` commands, no file writes to `<name>.Report/`. This room is pure planning. (Writing back to the brief itself IS allowed.)
- **Convert relative dates to absolute** when capturing decisions (e.g., "Q1" → "2026-Q1").

## What's here

- `brief-template.md` — **copy this** to start a new project brief
- `read-project-brief.md` — atomic step: how to read + merge briefs (folder vs single file)
- `brief-folder-structure.md` — when to use single file vs `brief/` folder; recommended layout
- `references/vague-prompts.md` — chat fallback intake script with anti-patterns
- `references/kpi-selection.md` — 20% change test, picking actionable measures
- `references/layout-patterns.md` — executive / operational / detail layouts with measurements
- `references/limitations.md` — what to tell the user the agent cannot do
