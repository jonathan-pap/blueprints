# Copy a theme from another report

Lift the active theme JSON from one project and apply to another.

## Procedure

```bash
# 1. Locate the source theme
SRC="<source-project>.Report"
SRC_THEME_NAME=$(jq -r '.themeCollection.customTheme.name' "$SRC/definition/report.json")
SRC_THEME_PATH="$SRC/StaticResources/RegisteredResources/$SRC_THEME_NAME"

# 2. Apply to target
pbir theme apply "<target-project>.Report" "$SRC_THEME_PATH"
```

## When the source is a thin report

Same procedure — themes live in `.Report/StaticResources/`, not in the model.

## When you want only the colors

Extract colors only and apply atop the target's existing theme:

```bash
# Read source colors
pbir theme colors "$SRC" -F json > /tmp/colors.json

# Apply to target's theme
pbir theme set-colors "<target-project>.Report" --from-json /tmp/colors.json
```

This preserves the target's text classes, visual-type overrides, etc.

## After

`../../report/validate/validate.md`.
