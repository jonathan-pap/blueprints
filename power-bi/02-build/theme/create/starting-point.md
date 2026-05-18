# Starting point

**Never author a theme from an empty `{}`.** You will miss properties Power BI depends on, and Desktop will silently fall back to defaults you didn't intend.

## Three valid starting points

### 1. SQLBI / Data Goblins theme (best for new authors)

Validated, complete, follows best practices. Lives at:

`../../report/examples/K201-MonthSlicer.Report/StaticResources/RegisteredResources/SqlbiDataGoblinTheme.json`

Or apply it directly with:

```bash
pbir theme apply-template "<project>.Report" sqlbi
```

### 2. Community templates (deldersveld / PowerBI-ThemeTemplates)

[github.com/deldersveld/PowerBI-ThemeTemplates](https://github.com/deldersveld/PowerBI-ThemeTemplates) has snippets for individual visual types. Cherry-pick patterns and assemble.

Best for: targeted overrides (e.g., a particularly nice slicer style) when you're extending an existing base.

### 3. Existing report theme (best when you have a reference report)

Export from Power BI Service via View → Themes → Save current theme, then extend.

```bash
# From a deployed report
fab get "<Workspace>.Workspace/<Report>.Report" -f | jq '.themeCollection.customTheme' > base-theme.json
```

Or copy from another local report — see `../apply/copy-from-other.md`.

## Decision

| You have... | Start with |
|---|---|
| Nothing | sqlbi template (option 1) |
| A reference report from a designer / consultant | Export it (option 3) |
| Brand guidelines but no theme yet | sqlbi (option 1), then customize colors + text classes |
| Specific visual style someone built before | Community templates (option 2) |

## After picking a base

Serialize into editable fragments before modifying — see `../serialize/split.md`. Do NOT edit the monolithic theme JSON directly.

```bash
pbir theme serialize "<project>.Report" -o /tmp/MyTheme.Theme
```

Edit fragments → build → apply back. See `from-scratch.md` for the full workflow.
