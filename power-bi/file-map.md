# File map — every artifact, its home, and its example

> The `.Report/` and `.SemanticModel/` paths are strict because Power BI fixes them. This file
> extends that same discipline to everything else the blueprint writes — templates, tokens, build
> scripts. **Before creating any file, find its row here.** Four different names for the same kind of
> file means the convention is missing, not that the file is special.

## The map

| Artifact | Lives at | Copy from / example | Governed by |
|---|---|---|---|
| Report (PBIR) | `projects/<name>/<name>.Report/` | `02-build/report/examples/K201-MonthSlicer.Report/` | [`02-build/report/pbip-format/_index.md`](02-build/report/pbip-format/_index.md) |
| Semantic model (TMDL) | `projects/<name>/<name>.SemanticModel/` | — | [`02-build/model/_index.md`](02-build/model/_index.md) |
| Desktop entry point | `projects/<name>/<name>.pbip` | created by `pbir new report` | [`projects/README.md`](projects/README.md) |
| Project brief | `projects/<name>/brief.md` (or `brief/`) | [`01-brief/brief-template.md`](01-brief/brief-template.md) | [`01-brief/read-project-brief.md`](01-brief/read-project-brief.md) |
| Layout tokens | `projects/<name>/design-system.yaml` | [`02-build/report/layout/design-system-default.yaml`](02-build/report/layout/design-system-default.yaml) | [`02-build/report/layout/design-system.md`](02-build/report/layout/design-system.md) |
| **Build scripts** | **`projects/<name>/build/`** | see [Build scripts](#build-scripts-the-durable-convention) below | [`02-build/report/tools/_index.md`](02-build/report/tools/_index.md) |
| A single visual | inside `<name>.Report/definition/pages/<page>/visuals/<id>/visual.json` | `02-build/report/examples/visuals/default/<type>.json` (20 bare) · `formatted/<type>.json` (35 styled) | [`02-build/report/examples/visuals/__index.md`](02-build/report/examples/visuals/__index.md) |
| Theme JSON | `projects/themes/` (shared) or the report's `StaticResources/` | `02-build/theme/examples/*.json` | [`02-build/theme/context.md`](02-build/theme/context.md) |
| Deneb / SVG / Python / R visual | inside the report, plus its spec/script | `02-build/visuals/<engine>/examples/` | [`02-build/visuals/context.md`](02-build/visuals/context.md) |
| Generated artifact (audit, export, trace) | `outputs/YYYY-MM-DD-<project>-<type>.<ext>` | — | [`outputs/README.md`](outputs/README.md) |

**Known gap:** there are per-visual templates but **no page-composition templates**. A page archetype
(KPI row + trend + detail) is currently rebuilt by hand or in script each time. If you find yourself
composing the same page shape twice, that's the missing library asking to be created — see
`layouts:` in `design-system.yaml`, which already names region templates.

## Build scripts — the durable convention

A scripted build is sanctioned ([`02-build/report/build-report.md`](02-build/report/build-report.md) B10).
Its **home and shape are fixed**, so builds stop inventing one:

```text
projects/<name>/
├── brief.md
├── design-system.yaml
├── <name>.Report/
├── <name>.SemanticModel/
├── <name>.pbip
└── build/
    ├── <name>kit.py      project specifics ONLY — palette, table names, bespoke recipes
    └── build.py          the entry point; re-runnable, rebuilds from brief + tokens
```

Rules:

- **Two file names, not four.** `build/<name>kit.py` and `build/build.py`. Never `_build-report.py`,
  `build_p1.py`, `finish_build.py`, `fix_layout.py` — a build step is a function in `build.py`, not a
  new file. (`build/` may hold extra modules for a genuinely large build; the entry point stays `build.py`.)
- **The kit holds only what is project-specific.** Anything a second project could use belongs in
  [`02-build/report/tools/pbirkit.py`](02-build/report/tools/pbirkit.py) — import, don't fork. A project
  kit is ~120–190 lines; if yours is growing past that, the excess is probably room-level.
- **`build.py` must be re-runnable.** Running it twice produces the same report. That is what makes the
  script an asset rather than a one-shot patch — the report becomes reproducible from brief + tokens.
- **Knowledge still lives in markdown.** A script may *enforce* a rule; the rule's home is always a
  `.md`. If a fact's only home is a `.py`, that's a bug.
- **Templates before code.** Reach for `examples/visuals/<type>.json` first; write Python only for what
  composition and repetition actually require.

## Appliers are swappable — the tool is not the doctrine

The durable truth is the **PBIR format** (a documented Microsoft schema) plus **our JSON templates**.
Everything that writes those files is an interchangeable applier:

| Applier | Can write? | Notes |
|---|---|---|
| [`tools/pbirkit.py`](02-build/report/tools/pbirkit.py) | **Yes** | Ours. Writes `visual.json` / `page.json` directly with `json.dump`. |
| `pbir` CLI | Yes | **Community, non-Microsoft, non-commercial licence.** Convenient, not authoritative. |
| `powerbi-report-author` (Microsoft) | **No** | `catalog` / `validate` / `preview-*` only — inspection, not authoring. Not a write fallback. |
| Plain file writes | Yes | Always available. A visual is a JSON file at a known path. |

**If `pbir` stops being maintained, the exposure is two calls.** The whole authoring core invokes it
only for `add page` and `pages rename` — and `add_page()` then rewrites `page.json` and `pages.json`
by hand anyway. Replacing it means: create the page folder, write `page.json`, append the id to
`pages.json` `pageOrder`. Everything else is already our own JSON writing.

The format is documented tool-independently, which is what makes that true:
[`schema-patterns/visual-json-structure.md`](02-build/report/schema-patterns/visual-json-structure.md) ·
[`expressions.md`](02-build/report/schema-patterns/expressions.md) ·
[`selectors.md`](02-build/report/schema-patterns/selectors.md) ·
[`property-catalogue.md`](02-build/report/schema-patterns/property-catalogue.md) ·
[`pbip-format/_index.md`](02-build/report/pbip-format/_index.md)

## Related

[`CLAUDE.md`](CLAUDE.md) (router) · [`projects/README.md`](projects/README.md) (raw layer) ·
[`outputs/README.md`](outputs/README.md) (output layer)
