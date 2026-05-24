# The `Copilot/` folder (Prep data for AI)

> Archival reference: Microsoft removed this from Learn on 2026-03-25 ("Remove Copilot tooling
> details from projects dataset"), but the folder still appears in PBIP projects saved with
> Copilot tooling enabled. Sourced from the pre-removal docs. Relevant when auditing a model's
> AI-readiness or diffing a `.SemanticModel` that contains it.

The `Copilot/` folder lives **inside `.SemanticModel/`** and holds everything configured via the
**Prep data for AI** button (Home ribbon, Desktop or service).

## Structure

```text
<Name>.SemanticModel/
  Copilot/
  ├── Instructions/
  │   ├── instructions.md          AI instructions (markdown)
  │   └── version.json
  ├── VerifiedAnswers/
  │   ├── definitions/<id>/
  │   │   ├── definition.json       trigger phrases, description
  │   │   ├── filters.json          filters applied to the visual
  │   │   └── visualSource.json     the visual that renders the answer (PBIR)
  │   └── version.json
  ├── schema.json                   AI data schema: visible tables/cols + synonyms
  ├── examplePrompts.json           suggested questions (Copilot "Zero Prompt")
  ├── settings.json                 top-level Copilot settings
  └── version.json
```

## Key files

| File | What it carries |
|---|---|
| `Instructions/instructions.md` | business context, terminology, analytical priorities for Copilot. **≤ 10,000 chars**, unstructured (interpreted, not guaranteed-adhered). Model-level, not report-level. |
| `schema.json` | which tables/columns Copilot can see + field synonyms |
| `VerifiedAnswers/definitions/<id>/` | a curated answer: trigger phrases + filters + a PBIR visual |
| `examplePrompts.json` | the starter questions shown on first open |

## Authoring & consumption

- **Author** via *Prep data for AI* in Desktop or the service. Desktop supports it for Import,
  DirectQuery, and Composite (local) only; all model types work in the service.
- **Consume** anywhere Copilot in Power BI exists.

## Git & deployment

- The `Copilot/` folder is committed to Git by default; include/exclude individual files via `.gitignore`.
- AI instructions + data schema also persist to LSDL (Linguistic Schema Definition Language).
- After a Git/pipeline deployment, sync needs a service refresh: Import = every deploy;
  DirectQuery / Direct Lake = once per day.
- After configuring, mark the model **Approved for Copilot** (service → Settings) to remove
  friction treatment for that model and its reports.

## Related

- [what-is-pbip.md](what-is-pbip.md) — the rest of the PBIP folder layout
- [../../../04-review/model-audit/ai-readiness.md](../../../04-review/model-audit/ai-readiness.md) — auditing a model for Copilot/Q&A readiness
