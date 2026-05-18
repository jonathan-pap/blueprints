# Graceful degradation

Hooks defensively exit 0 (skip silently) on any environmental failure rather than block. Validation is best-effort; the cost of a false block is much higher than a missed check.

## Skip conditions

| Condition | Hooks affected | Why |
|---|---|---|
| `jq` not on `PATH` | all | Every hook needs jq to parse stdin and `tmp/model-metadata.json` |
| `pbi-hooks.sh` not found at `${CLAUDE_PLUGIN_ROOT}/hooks/pbi-hooks.sh` | all (Claude Code skips invocation) | Hook can't even start |
| `tmp/model-metadata.json` missing | `validate-dax`, `check-ri`, `check-compat` | No cache to validate against — first connect populates it |
| `tmp/model-metadata.json` corrupt or unparseable | `validate-dax`, `check-ri`, `check-compat` | jq returns empty → all checks no-op |
| Neither `powershell.exe` nor a running Parallels VM | `refresh-cache`, `check-ri`, `check-compat` auto-upgrade | Can't reach the live model |
| `config.yaml` missing | none | All checks default to enabled — same as `all_hooks_enabled: true` |
| `config.yaml` `all_hooks_enabled: false` | all | Master kill-switch — see `config.md` |

## What this means in practice

- **First TOM connect of a project**: `refresh-cache` populates `tmp/model-metadata.json`. Before that snapshot exists, `validate-dax` skips — no model-aware validation on the first command of a session.
- **Stale cache**: if the model was modified externally (Power BI Desktop UI, another agent, etc.) between TOM connects, `validate-dax` is checking against an older snapshot. Refreshes happen automatically on the next TOM connect or `SaveChanges`.
- **Cache stuck stale**: if `refresh-cache` itself fails (PowerShell unavailable, port not extractable), the cache is never updated. The hook exits 0 silently — no error is shown. Run the snapshot script manually if you suspect this.

## Manual cache refresh

```bash
powershell.exe -ExecutionPolicy Bypass \
  -File hooks/snapshot-model.ps1 -Port <PORT> -OutFile ./tmp/model-metadata.json
```

The port comes from `(Get-WmiObject Win32_Process -Filter "Name='msmdsrv.exe'").CommandLine` or `Get-Content "$env:LOCALAPPDATA\Microsoft\Power BI Desktop\AnalysisServicesWorkspaces\*\Data\msmdsrv.port.txt"` — see `../quickstart.md`.
