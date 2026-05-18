# 01-brief/hooks/ — brief discovery

## What this does

`discover-briefs.sh` is a **UserPromptSubmit** hook. On every user prompt, it scans `power-bi/projects/**/brief.md` (and the folder form `power-bi/projects/**/brief/*.md`) for files modified within a threshold and emits a `<recent-briefs>` block as additional context. Claude then reads any flagged brief before asking discovery questions or proposing a plan.

Catches:
- New brief created in the IDE between turns
- Existing brief edited in the IDE between turns
- Brief that exists but Claude hasn't seen yet this session

## Toggle

`power-bi/hooks.yaml`:

```yaml
briefs: false   # disable the hook (default: true)
```

Adjust the threshold via env var:

```bash
BRIEF_DISCOVERY_MINUTES=180   # 3-hour window instead of 60-minute
```

## Register in Claude Code (`settings.json`)

This hook requires UserPromptSubmit registration in your harness config. Add to `~/.claude/settings.json` (global) or `<project>/.claude/settings.json` (per-project):

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash \"${CLAUDE_PROJECT_DIR}/power-bi/01-brief/hooks/discover-briefs.sh\"",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

Or use the `update-config` skill: ask Claude to "register the brief discovery hook in settings.json".

## Verify

After registration, start a new conversation and `touch power-bi/projects/<name>/brief.md`. The next user prompt should include a `<recent-briefs>` block — Claude will mention it has spotted recent briefs.

Manual test (no Claude Code required):

```bash
bash power-bi/01-brief/hooks/discover-briefs.sh
# Outputs <recent-briefs>...</recent-briefs> if any briefs were touched in the last 60min
# Silent (exit 0) if none
```

## Cost

One `find` over `projects/` per prompt. With ~20 projects, negligible (~10-20ms). Output adds ~50-200 tokens per matching brief.

## See also

- [`../brief-template.md`](../brief-template.md) — project (report) brief template
- [`../../02-build/theme/create/brief-template.md`](../../02-build/theme/create/brief-template.md) — theme brief template
- [`../../hooks.yaml`](../../hooks.yaml) — master toggle (`briefs:`)
- [`../read-project-brief.md`](../read-project-brief.md) — file-first / chat-second pattern
