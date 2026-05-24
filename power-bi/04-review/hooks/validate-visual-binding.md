# validate-visual-binding hook

PreToolUse hook that catches **hallucinated field names** in `pbir add visual` / `pbir visuals bind` commands before they create broken visuals.

## The failure mode it prevents

```text
User: "Add a KPI for Gross Profit Margin"
Claude: pbir add visual kpi ... -d "Indicator:_Measures.Gross Profit Margin"
pbir:   (no validation; writes broken JSON)
Open Desktop: visual renders blank, no error
```

The actual measure was `Profit %`. Without this hook, the broken binding only surfaces when you reopen the report.

## How it works

1. Fires on `Bash(*pbir add visual*)` or `Bash(*pbir visuals bind*)` (PreToolUse).
2. Extracts every `-d "role:Table.Field"` argument from the command.
3. Resolves the Report path from the command, runs `pbir model "<report>" -d` to enumerate real fields.
4. For each `Table.Field`, checks that `Field` appears as a bullet entry in the model output.
5. If any field is missing: exit 2 with stderr listing the failures + closest-match suggestions.

The block looks like:

```text
Visual binding validation failed:
  Field not found in model: '_Measures.Gross Profit Margin'
    Did you mean:
    → Profit %
Run `pbir model "<report>" -d` to list real fields before retrying.
```

## Toggles

- **Parent** (`power-bi/hooks.yaml` → `review: false`) — disables the whole 04-review/hooks subsystem
- **Per-hook** (`config.yaml` → `binding_check: false`) — disables just this check

## Skip conditions (exits 0 silently)

- `pbir` not on PATH
- `pbir model -d` fails (thin report or unreachable model)
- Neither `jq` nor `python` available
- Stdin not parseable as hook JSON

Defensive by design — false-positive blocks are worse than missed validations.

## Test by hand

```bash
echo '{"tool_name":"Bash","tool_input":{"command":"pbir add visual kpi \"power-bi/projects/test/test.Report/Some.Page\" -d \"Indicator:_Measures.Fake Measure\""}}' | \
  bash power-bi/04-review/hooks/validate-visual-binding.sh
echo "exit=$?"
```

Expect `exit=2` with a "Field not found" message.

## See also

- `../../02-build/report/bind/find-canonical-name.md` — the prevention layer (always check field names FIRST)
- `validate-pbir.sh` — companion hook that validates PBIR JSON structure after Write/Edit
