# config.yaml — toggle checks

All checks are enabled by default. Edit `config.yaml` next to `pbi-hooks.sh`. Changes take effect immediately (hooks re-read on every invocation; no restart needed).

## Keys

| Key | Default | Effect when `false` |
|---|---|---|
| `all_hooks_enabled` | `true` | Master kill-switch — skips every hook in this plugin, leaves individual toggles intact |
| `dax_validation` | `true` | `validate-dax` skips — DAX refs are no longer checked against the model |
| `measure_metadata` | `true` | `validate-measure` skips — `.Measures.Add` calls no longer require DisplayFolder/Description/FormatString |
| `metadata_refresh` | `true` | `refresh-cache` skips — `tmp/model-metadata.json` becomes stale; other validators silently no-op once stale |
| `referential_integrity` | `true` | `check-ri` skips — orphan keys after relationship/column changes go unreported |
| `compatibility_check` | `true` | `check-compat` skips — no nudge about features available at a higher CL |
| `compatibility_auto_upgrade` | `false` | When `true`, `check-compat` auto-upgrades the model CL to the engine max. **Irreversible.** Default is off for a reason. |

## Disabling for one session

The hook's blocking error message always includes the absolute `config.yaml` path so you can flip a single check without grep-hunting:

```text
DAX validation failed: Table 'Saless' does not exist in the model.
Did you mean 'Sales'? (Set dax_validation: false in
/path/to/hooks/config.yaml to disable this check.)
```

## When to flip `all_hooks_enabled`

- Noisy `PreToolUse hook error` on Windows (see `windows-issues.md`)
- Debugging an unrelated tool — clean stderr is more useful than partial validation
- Working offline / against a model you intentionally don't want validated

Flip back to `true` once the noise source is fixed.
