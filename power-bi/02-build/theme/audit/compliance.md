# Audit theme compliance

Does each visual inherit from the theme cleanly, or has it accumulated bespoke overrides?

## CLI

```bash
pbir audit theme "<project>.Report"
```

Reports per-visual compliance: how many properties are theme-driven vs visual-overridden.

## Read the output

For each visual:

- **Inherits cleanly** — no `objects` / `visualContainerObjects` overrides. Theme controls everything.
- **Minor drift** — 1–3 overrides. Usually intentional (content-specific tweaks).
- **Heavy drift** — > 5 overrides. Investigate. Often the result of bespoke per-visual formatting that should be promoted.

## When the theme itself is the problem

A report using the default Power BI theme (or a minimal custom theme with just `dataColors` and a name) will show drift everywhere — there's nothing for visuals to inherit. The fix is to author a real theme: `../modify/wildcard.md` + `../modify/visual-type-override.md` for the common types.

## Output to file

```bash
pbir audit theme "<project>.Report" -o ../../../outputs/$(date +%Y-%m-%d)-<project>-theme-compliance.md
```

## See also

- `find-overrides.md` — list which visuals have which overrides
- `find-hardcoded-hex.md` — find hex colors that should reference theme colors
- `../promote/from-visuals.md` — fix the drift by lifting it to the theme
