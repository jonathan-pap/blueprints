# tools/ — room-level Python helpers for scripted PBIR builds

Shared code that every scripted report build imports. **One copy, here** — a project folder holds
only its palette, table names, and bespoke recipes (the rule: rooms are the workflow, `projects/`
is data). If a helper is useful to a second project, it belongs here, not copied.

- `pbirkit.py` — the PBIR authoring core: `configure()` binds it to a project (root, `.Report`
  name, fact/measure tables, palette, `design-system.yaml`); then `rects`/`stack`/`inset`
  (geometry from the grid), `lit`/`solid`/`measure`/`col`/`proj_m`/`proj_c` (expressions +
  projections), `vis`/`textbox`/`head_tb`/`heading`/`image_svg`/`slicer` (visual JSON),
  `panel`/`noframe`/`axis`/`sort_by`/`in_filter` (formatting + filters), `add_page`/`write`/`run`
  (pages, files, `pbir` calls). Docstring shows the 6-line project wiring.
- `resolve_layout.py` — regions → snapped pixel rects from a project's `design-system.yaml`
  (CLI: `python resolve_layout.py <design-system.yaml> [layout …]`).

Worked users: `projects/telecom-churn/churnkit.py`, `projects/arcane-emporium/emporiumkit.py`
(each ~120–150 lines of project-specific code on top of this core).
