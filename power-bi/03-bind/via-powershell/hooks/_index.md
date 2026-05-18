# hooks/ — Live-model validation hooks

> PreToolUse / PostToolUse hooks that validate DAX references, enforce measure metadata, snapshot model metadata, check referential integrity, and report compatibility-level upgrades — all against the **live** Power BI Desktop model via TOM/ADOMD.NET.

Different from [`../../../04-review/hooks/`](../../../04-review/hooks/), which validates PBIR/TMDL **files on disk** after Write/Edit. These hooks fire on Bash commands that touch the live model.

## Hook files

- `pbi-hooks.sh` — main dispatcher (5 subcommands)
- `snapshot-model.ps1` — captures model metadata to `tmp/model-metadata.json` for validators to read
- `check-referential-integrity.ps1` — runs EXCEPT queries to find orphan keys after relationship/column changes
- `hooks.json` — Claude Code hook registration (event + matcher + `if` filter per hook)
- `config.yaml` — toggle individual checks or kill-switch all hooks

## Docs

- `overview.md` — what each of the 5 hooks does and when it fires
- `config.md` — toggleable checks via `config.yaml`
- `degradation.md` — what happens when dependencies (jq, PowerShell, Parallels) are missing
- `windows-issues.md` — Claude Code bugs that affect Bash hooks on Windows + master kill-switch
- `testing.md` — how to fire a hook by hand

## Install

Hooks register through Claude Code's plugin / hooks mechanism. Copy `hooks.json` into your harness config (e.g., `.claude/hooks.json`) and point `${CLAUDE_PLUGIN_ROOT}/hooks/pbi-hooks.sh` at this folder. `jq` must be on `PATH`; PowerShell is auto-detected (or routed via Parallels on macOS — see `../parallels-macos.md`).
