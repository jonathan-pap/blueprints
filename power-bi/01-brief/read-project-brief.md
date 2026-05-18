# Read a project brief

Atomic step for the agent. Runs FIRST in any `01-brief/` workflow — before `AskUserQuestion`, before `vague-prompts.md` defaults.

## Lookup order

For a project at `projects/<name>/`:

1. **`projects/<name>/brief/` folder exists?** → read every `*.md` in it (alphabetical order). Folder beats single file.
2. **Otherwise `projects/<name>/brief.md` exists?** → read that single file.
3. **Otherwise no brief exists** → proceed with conversational discovery per `context.md` (`vague-prompts.md` defaults).

## What to extract

From whichever form the brief takes, build a structured mental model with these sections (matching `brief-template.md`):

1. **Audience & decision** — drives KPI selection + layout
2. **Source data & model** — thick vs thin PBIP, refresh cadence, capacity
3. **KPIs** — measure names, target sources, formats
4. **Pages & layout** — page count, per-page visual plan
5. **Branding & style** — theme choice, colors, fonts, logo
6. **Constraints & non-goals** — perf, accessibility, page size, scope cuts
7. **Open questions** — surface these as the FIRST `AskUserQuestion`s
8. **References** — existing reports, source docs

## Fill the gaps (not the basics)

The brief tells you what the user already decided. Do NOT re-ask those. Only `AskUserQuestion` for:

- Items in the brief's "Open questions" section (Section 7).
- Sections that say `[fill in]` or are missing entirely.
- Ambiguities you genuinely can't resolve from context (e.g., brief lists "Margin" but doesn't specify Gross / Net / Standard).

Cap to 3 questions per `vague-prompts.md`. If the brief is comprehensive, you may have ZERO follow-up questions — proceed straight to "propose layout".

## Propose, then lock

Same as the no-brief workflow: present the concrete plan via `AskUserQuestion` with a "yes / change X" choice. Once locked, write a final "locked brief" summary back to the project (either updating `brief.md` or appending to `brief/00-locked-decisions.md`).

## Multi-brief precedence

If `projects/<name>/brief/` has multiple files, the **alphabetical order** is the load order. Numbered prefixes (`00-context.md`, `01-kpis.md`, …) make this deterministic. Last file wins on conflicting fields, but the agent should flag conflicts and ask the user to resolve rather than silently picking.

## When the brief is stale

Briefs decay. If the brief references measure names that no longer exist in the model, page layouts that don't match what's in `<name>.Report/`, or KPIs that don't appear in the model:

- Flag the discrepancy to the user.
- Ask whether to update the brief to match reality, or rebuild reality to match the brief.
- Don't silently proceed against a stale brief — the wrong decisions get locked in.

## Sample brief location for `test` project

See `../../projects/test/brief.md` for a worked example.
