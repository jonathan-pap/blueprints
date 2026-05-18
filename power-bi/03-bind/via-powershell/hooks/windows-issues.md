# Known Windows issues + master kill-switch

Claude Code has several open bugs that affect Bash hooks on Windows. Spurious `PreToolUse:Bash hook error` / `PostToolUse:Bash hook error` notices on commands that clearly shouldn't match any `if` filter (e.g., `mkdir`, `ls`, `cat`) usually mean you're hitting one of these.

## Open bugs

| Bug | Effect |
|---|---|
| [anthropics/claude-code#49229](https://github.com/anthropics/claude-code/issues/49229) | The `if` field is silently ignored; every Bash matcher entry spawns for every Bash call |
| [#38800](https://github.com/anthropics/claude-code/issues/38800) | `${CLAUDE_PLUGIN_ROOT}` expansion breaks when the user path contains spaces |
| [#47070](https://github.com/anthropics/claude-code/issues/47070) | `execvpe(/bin/bash)` fails on Windows with Docker Desktop but no full WSL distro |
| [#50243](https://github.com/anthropics/claude-code/issues/50243) | Bash hooks silently not invoked on Windows with `settings.local.json`-only config |
| [#34457](https://github.com/anthropics/claude-code/issues/34457) | Hooks with shell commands cause 5+ minute hangs/crashes on Windows |

## Defensive design

Hook scripts in this plugin exit 0 on any environmental failure so the errors are cosmetic — commands still run, the validation just doesn't fire. Nothing is silently broken; nothing is silently skipped at the model level.

## Master kill-switch

If the noise bothers you, flip the kill-switch in `config.yaml`:

```yaml
all_hooks_enabled: false
```

This disables every hook in this plugin without touching individual check toggles. Flip back to `true` once you upgrade to a Claude Code build that resolves the underlying bugs.

## Other known limitations

- **`.ps1` file execution hides content from `if` filters** — hooks only validate inline PowerShell commands; for `-File <path>.ps1` invocations, the dispatcher reads the file content itself to apply the same checks.
- **`if` glob patterns are case-sensitive** — `Bash(*SaveChanges*)` matches but `Bash(*savechanges*)` does not.
- **UNC path conversion assumes `/Users/<user>/` prefix** on macOS Parallels — adjust `convert_to_exec_path` in `pbi-hooks.sh` if your home is elsewhere.
