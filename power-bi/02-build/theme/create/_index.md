# create/ — author a theme from scratch

> Full workflow for creating a new theme. **Never author from an empty `{}`** — always start from a validated base. See `starting-point.md`.

## Brief first (if it exists)

Before walking the workflow, check for `projects/themes/<theme-slug>/brief.md`. If present, read it and fill any `[fill in]` gaps via `AskUserQuestion` BEFORE entering the workflow. If absent and the user has decisions to capture, offer to scaffold one from `brief-template.md`.

## Workflow

1. **Pick a starting point** → `starting-point.md`
2. **Add the schema reference** → `schema-integration.md`
3. **Design the color system** (4 layers in order) → `color-system.md`
4. **Set typography** → `typography-roles.md`
5. **Set wildcard container defaults** → `wildcard-defaults.md`
6. **Override critical visual types** (textbox, image, shape, button) → `visual-type-priorities.md`
7. **Validate against the checklist** → `checklist.md`

For where the resulting theme JSON gets stored on disk: `../where-themes-live.md`.

## After creation

Once the theme exists and is in the report:

- **Apply to a different report** → `../apply/file.md` or `../apply/copy-from-other.md`
- **Tweak colors / text classes** → `../modify/colors.md`, `../modify/text-classes.md`
- **Add or change visual-type overrides** → `../modify/visual-type-override.md`
- **Audit drift** → `../audit/_index.md`
- **Promote visual-level formatting back into theme** → `../promote/_index.md`

## Hard rules (apply during creation)

- **Never read the full monolithic theme JSON.** Files can hit 75 KB / 2000+ lines. Always serialize first (`../serialize/split.md`) or use `jq` to extract specific keys.
- **`$schema` first key** — enables IDE autocomplete + Desktop validation on import.
- **`dropShadow.show: false` in wildcard** — global default; only enable on specific visual types that benefit.
- **Custom fonts will not render on other users' machines** — Segoe UI / Segoe UI Semibold only.
