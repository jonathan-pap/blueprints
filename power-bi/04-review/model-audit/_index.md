# model-audit/ — atomic files

> Structured evaluation of a semantic model against quality, performance, and best-practice standards.

## Foundation

- `audit-workflow.md` — Step 0–4: gather context, analyze structure, run checks, report findings
- `gather-context.md` — what to ask the user BEFORE analyzing TMDL

## Checks (by category)

- `categories.md` — full check catalog by severity (Critical / Memory / DAX / Documentation / Design / Direct Lake / AI)
- `ai-readiness.md` — Copilot + data agent readiness checklist
- `performance.md` — model-level perf testing methodology

## Tooling

- `model-info-script.md` — `get_model_info.py` wrapper for storage mode, size, lineage, refresh, capacity
- `scripts/get_model_info.py` — the script

## When to enter

User asks: "review a semantic model", "audit a semantic model", "check model quality", "optimize my model", "validate model design", "check AI readiness", "prepare model for Copilot".

## Related rooms

- For the auditor agent that runs the categories — `../reviewers/semantic-model-auditor.md`
- For DAX-specific optimization (after audit) — `../../02-build/model/dax/`
- For naming fixes (a common audit finding) — `../../02-build/model/naming/`
- For lineage / downstream impact — `../lineage/`
- For refresh diagnostics — `../../03-bind/via-powershell/refresh-troubleshooting.md`
