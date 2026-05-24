# 01-brief/hooks/ — brief discovery

## What this does

`discover-briefs.sh` is a **UserPromptSubmit** hook. On every user prompt it scans
`synthetic-data/projects/**/brief.md` (and the folder form `**/brief/*.md`) for files modified
within a threshold and emits a `<recent-briefs>` block as additional context. Claude then reads
any flagged job brief before asking discovery questions or proposing a plan.

Catches:

- New brief created in the IDE between turns
- Existing brief edited in the IDE between turns
- Brief that exists but Claude hasn't seen yet this session

The script is **portable** — it derives the blueprint name from its own path, so it's identical
to `power-bi/01-brief/hooks/discover-briefs.sh`. Copy it into any new blueprint's `01-brief/hooks/`.

## Toggle

`synthetic-data/hooks.yaml`:

```yaml
briefs: false   # disable the hook (default: true)
```

Adjust the threshold via env var:

```bash
BRIEF_DISCOVERY_MINUTES=180   # 3-hour window instead of 60-minute
```

## Register in Claude Code (`settings.json`)

This hook requires UserPromptSubmit registration. The workspace `.claude/settings.json` already
registers both blueprints' hooks side by side:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          { "type": "command", "command": "bash \"${CLAUDE_PROJECT_DIR}/power-bi/01-brief/hooks/discover-briefs.sh\"", "timeout": 5 },
          { "type": "command", "command": "bash \"${CLAUDE_PROJECT_DIR}/synthetic-data/01-brief/hooks/discover-briefs.sh\"", "timeout": 5 }
        ]
      }
    ]
  }
}
```

Both run on every prompt; each is silent unless its own `projects/` has a recently-touched brief.
Or use the `update-config` skill: ask Claude to "register the synthetic-data brief discovery hook".

## Verify

After registration, start a new conversation and `touch synthetic-data/projects/<job>/brief.md`.
The next prompt should include a `<recent-briefs>` block.

Manual test (no Claude Code required):

```bash
bash synthetic-data/01-brief/hooks/discover-briefs.sh
# Outputs <recent-briefs>...</recent-briefs> if any briefs were touched in the last 60min
# Silent (exit 0) if none
```

## Cost

One `find` over `projects/` per prompt — negligible (~10-20ms). Output adds ~50-200 tokens per
matching brief.

## See also

- [`../brief-template.md`](../brief-template.md) — job brief template
- [`../../hooks.yaml`](../../hooks.yaml) — master toggle (`briefs:`)
- [`../context.md`](../context.md) — the brief room (file-first / chat-second)
