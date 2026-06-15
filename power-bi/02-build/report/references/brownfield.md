# Brownfield redesign

> Read this when redesigning, restyling, theme-swapping (light↔dark), modernizing, or critiquing an
> **existing** report. The [identity-workflow](../build-report.md) Steps 0→7 still all run — but each
> runs in **delta-against-current** mode, not from a blank canvas.

## When this applies

"redesign this report" · "restyle the visuals" / "make it look professional" · "switch to dark mode" /
"convert to light" · "apply our brand" · "modernize this" · "the visuals don't match the rest" / "fix
the design of [page]". If unclear (a screenshot but no explicit ask), **ask** before proceeding.

## Entry workflow

1. **Load** — confirm the existing PBIP path. Read the current theme + `design-system.yaml`.
2. **Capture "before"** — inventory each page's visuals ([`pbir preview-visuals`](../validate/validate.md));
   if Desktop is open, screenshot each page as before-evidence.
3. **Diagnose** the current report against [anti-patterns.md](anti-patterns.md),
   [accessibility.md](accessibility.md), and the new target identity ([tones.md](tones.md) /
   [signatures.md](signatures.md)) — compute the gap.
4. **Emit a re-design brief** (`mode: brownfield`) — list the specific pages, visuals, theme entries,
   and chrome that change, each with a rationale. Preserve bookmarks/visual links unless explicitly
   retired; flag any that target ids that change.
5. **Hand off** the surgical edits to [`../context.md`](../context.md); validate after each batch
   ([`../validate/validate.md`](../validate/validate.md)).
6. **Final audit** — screenshot AFTER; verify the target tone landed without breaking what worked.

## How each step changes in brownfield mode

| Step | Greenfield | Brownfield delta |
|---|---|---|
| 0 Data | inspect model fresh | usually unchanged — same model |
| 1 Identity | commit tone + signature | capture **`current_tone`/`current_signature`** AND target; the delta drives the plan |
| 2 Archetype | route per page | **audit** existing pages vs the archetype rules + new identity; re-route or accept-and-document |
| 3–4 Charts | select & configure | **preserve useful visuals**; replace only when a visual no longer serves the question/identity |
| 5 Theme | adapt to identity | compute a theme **delta** — which palette entries / `textClasses` / `visualStyles` change. Don't rebuild ([`../../theme/audit/find-overrides.md`](../../theme/audit/find-overrides.md)) |
| 6 Brief | greenfield brief | re-design brief — same [contract](../layout/design-contract.md), `mode: brownfield`, brownfield fields filled |
| 7 Review | pre-flight | + the brownfield items below |

## Brownfield pre-flight (in addition to the standard checklist)

- [ ] **Removed/replaced visuals reasoned about** — every visual that disappears or changes type is in the brief, not silently dropped.
- [ ] **Conditional-formatting logic preserved** — a palette/dark↔light swap doesn't invalidate CF rules that reference palette slots; thresholds + colour expressions still resolve.
- [ ] **Contrast re-validated** — for any light↔dark swap, every previously-compliant text/bg pair is still compliant ([accessibility.md](accessibility.md#contrast--formula--thresholds)).
- [ ] **Bookmarks survive id changes** — if visuals are renamed/replaced, every bookmark referencing the old id is updated or retired (`pbir validate` catches structure; verify `visualLink` targets manually).
- [ ] **Page background re-checked** — dark themes need a darker page background than the default; confirm it contrasts with the new visual containers.

## Theme-swap shortcut (light ↔ dark)

For a pure swap with no other redesign, follow the consolidated checklist:
**[`../../theme/modify/dark-mode-checklist.md`](../../theme/modify/dark-mode-checklist.md)** — it covers the
polarity gate (hardcoded foreground text doesn't follow the theme), the `#FFFFFF` dual-meaning trap,
`stylePreset:'None'` on every table, the azureMap style enum, and the per-visual sweep. Build a
sibling theme with inverted neutrals + an adjusted palette; sweep inline overrides via
[`../../theme/audit/find-hardcoded-hex.md`](../../theme/audit/find-hardcoded-hex.md).

## Related
- [identity-workflow.md](../build-report.md) — the Steps this runs in delta mode
- [`../../theme/modify/dark-mode-checklist.md`](../../theme/modify/dark-mode-checklist.md) · [`../../theme/audit/find-hardcoded-hex.md`](../../theme/audit/find-hardcoded-hex.md) · [`../../theme/audit/find-overrides.md`](../../theme/audit/find-overrides.md)
- [anti-patterns.md](anti-patterns.md) · [accessibility.md](accessibility.md)
