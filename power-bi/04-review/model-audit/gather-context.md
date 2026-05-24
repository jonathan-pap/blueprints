# Gather context (Step 0)

**Before analyzing TMDL, ask the user.** A model audit is meaningless without context — the same finding can be critical in one model and ignorable in another.

## Run the model info script first

```bash
python scripts/get_model_info.py -w <workspace-id> -m <model-id>
```

Returns: storage mode (Import / DirectQuery / Direct Lake), model size, connected reports, deployment pipeline stage, endorsement status (certified / promoted), sensitivity label, data sources, refresh schedule, last refresh status, capacity SKU.

This is mechanical context. It tells you "what is the model"; you still need to ask "what is the model FOR".

## Ask the user (`AskUserQuestion`)

1. **What business process does this model represent?**
2. **Who are the primary consumers?** Report developers, analysts, executives, AI/Copilot users?
3. **Are they the developer of both the model and its reports, or only one?**
4. **Is the model in development, testing, or production?**
5. **Where should findings be documented?** scratchpad, agent-docs, wiki, etc.

## Why context shifts severity

A model for 3 analysts has very different requirements than one consumed by Copilot across the org.

- **Many low-skill users + Copilot consumption** → naming, descriptions, AI instructions become CRITICAL.
- **Small power-user team** → naming polish is suggestion, performance + correctness are critical.
- **Production model with many downstream reports** → any structural change is high-risk; audit recommendations skew conservative.
- **Dev/test model** → speculative recommendations OK; encourage experimentation.

## Output location decision

Where you save the audit affects how it gets used:

- `../../outputs/YYYY-MM-DD-<model>-audit.md` — standard place, per `CLAUDE.md` naming convention
- Project README — only if the user wants the findings persistent across sessions
- Issue tracker / wiki — only if the user explicitly asks; involves auth + external tools

Default: `outputs/`. Ask if anything else.

## Don't skip this step

Audits without context produce generic check-the-box reports that miss the actual problems. The 10 minutes of questions before analysis save hours of writing irrelevant findings.
