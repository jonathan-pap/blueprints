# Full report audit

One-shot audit via `pbir audit`. Returns a structured report covering structure, bindings, theme compliance, and known anti-patterns.

## Command

```bash
pbir audit "<project>.Report" -o ../../outputs/$(date +%Y-%m-%d)-<project>-audit.md
```

## What it checks

- Structural: every visual.json, page.json, report.json validates against Microsoft's PBIR schemas.
- Bindings: every visual references real model fields (when model is reachable).
- Theme compliance: how many visuals override theme defaults.
- Anti-patterns: overlapping visuals, missing titles, hardcoded hex colors, no theme applied.
- File hygiene: UTF-8 BOM check, folder name issues.

## What it does NOT check

- Live DAX validity (use `../../03-bind/via-mcp/validate-dax.md`).
- Live model data correctness.
- Visual aesthetic / design quality (manual — see `visual-design.md`).
- Usage / adoption (see `../usage/`).

## Reading the output

Severity levels:
- **CRITICAL** — broken visual, missing required schema field. Block release.
- **WARNING** — anti-pattern (overlapping visuals, missing title, no theme). Fix before release.
- **INFO** — suggestion (consider promoting overrides to theme).

## After

For each finding, route to the matching workflow:
- Missing title → `../../02-build/report/page/add-page-title.md`
- Hardcoded hex → `../../02-build/theme/audit/find-hardcoded-hex.md`
- Missing theme → `../../02-build/theme/apply/template.md`
- Broken field → `../../02-build/report/validate/fix-broken-field-reference.md`
