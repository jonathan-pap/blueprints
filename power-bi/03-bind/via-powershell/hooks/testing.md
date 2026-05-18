# Test a hook by hand

Hooks read JSON from stdin and follow Claude Code's exit-code convention (0 = OK, 2 = block). Fire one directly to verify it works without going through Claude Code.

## Fire a single subcommand

```bash
echo '{"tool_name":"Bash","tool_input":{"command":"EVALUATE '"'"'FakeTable'"'"'[Col]"}}' | \
  CLAUDE_PROJECT_DIR="$(pwd)" \
  CLAUDE_PLUGIN_ROOT="$(pwd)/03-bind/via-powershell" \
  bash 03-bind/via-powershell/hooks/pbi-hooks.sh validate-dax
```

Exit code 0 = the hook ran and either passed or skipped. Exit code 2 = the hook blocked (stderr contains the reason).

## What to test

| Subcommand | Stdin tool_input.command | Expected outcome |
|---|---|---|
| `validate-dax` | command containing `'BadTable'[X]` | Exit 2, "Table 'BadTable' does not exist" |
| `validate-dax` | command containing `'RealTable'[BadCol]` | Exit 2, "Column [BadCol] does not exist in 'RealTable'" + suggestion |
| `validate-dax` | command with no DAX context | Exit 0 (skipped via `has_dax_context`) |
| `validate-measure` | command containing `.Measures.Add(...)` with no metadata | Exit 2, lists missing properties |
| `validate-measure` | command containing `.Measures.Add(...)` with all metadata | Exit 0 |
| `refresh-cache` | command containing `localhost:1234` and `Microsoft.AnalysisServices` | Exit 0; check `tmp/model-metadata.json` updated |
| `check-ri` | command containing `SaveChanges` and `Relationship` | Exit 0 or 2 depending on whether the live model has orphans |
| `check-compat` | any `-File *.ps1` command | Exit 0 (no upgrade available) or 2 (lists features at higher CL) |

## Pre-requisites for end-to-end tests

- `tmp/model-metadata.json` exists (run `refresh-cache` first against a live model)
- `jq` on `PATH`
- For `check-ri` / `check-compat` / `refresh-cache` → live Power BI Desktop with a model loaded on a known port

## CI integration

These hooks are designed to run against a live model and skip silently otherwise — they are not suitable for headless CI. Use [`../../../04-review/hooks/`](../../../04-review/hooks/) (PBIR/TMDL file validation) for CI; it runs against files on disk and doesn't need a running Desktop.
