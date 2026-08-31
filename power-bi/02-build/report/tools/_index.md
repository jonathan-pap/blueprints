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

CLI utilities (run, not imported):

- `convert_legacy_to_pbir.py` — legacy monolithic `report.json` → PBIR directory format
  (doctrine: [`../validate/convert-legacy.md`](../validate/convert-legacy.md))
- `set-background-image.py` — apply an image as a page wallpaper, sized correctly
- `generate-background-with-gemini.py` — OPTIONAL: Gemini-generated background from a text prompt —
  the one script with an external AI dependency; nothing else depends on it
  (both: [`../page/set-page-wallpaper.md`](../page/set-page-wallpaper.md))

**Hard rule:** a script here may *enforce* a rule, but the rule's home is always a markdown file.
If a fact's only home is a `.py`, that's a bug (see build trap 15 for the precedent).

**Templates before code.** Compose from `../examples/visuals/<type>.json` first; write Python only for
what repetition and composition actually require. A build that could have been templates plus a few
CLI calls shouldn't become a script.

## Where a project's own code goes

Fixed shape, so builds stop inventing one ([`../../../file-map.md`](../../../file-map.md)):

```text
projects/<name>/build/
├── <name>kit.py      project specifics only — palette, table names, bespoke recipes
└── build.py          entry point; re-runnable (twice = same report)
```

Worked users: `projects/telecom-churn/churnkit.py`, `projects/arcane-emporium/emporiumkit.py` —
each ~120–190 lines of project-specific code on top of this core. Both predate the `build/` convention
and still sit at their project root; new projects use `build/`.
