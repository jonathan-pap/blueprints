# test — live recipe proving-ground

The scratch PBIP where every `02-build/recipes/*` pattern gets **battle-tested live** before
it's trusted. Not a deliverable — a lab. Pages get wiped and rebuilt freely.

Open `test.pbip` in Power BI Desktop to view. After any script run, **close and reopen** —
Desktop does not detect external file changes.

## Why the `_build-*.py` scripts exist

The PBIR/TMDL format is **generated, not authored**, and Power BI Desktop actively rewrites
it on save. Hand-editing fights both. Each script turns a fragile, multi-file, Desktop-hostile
edit into **one replayable build step**. Five reasons:

1. **The format is a file *tree*, not a file.** One gallery page = `page.json` +
   `visuals/<id>/visual.json` per visual, each needing a unique 20-char id, a computed
   `position`, and a deep `query`/`objects` tree. The native gallery laid out ~30 visuals
   across 6 pages. A loop with `vid()` + a `grid()` layout function writes that from one
   source of truth — and the no-overlap tiling is *computed*, not eyeballed.

2. **Desktop clobbers what you type.** With the `.pbip` open, Desktop re-saves the whole
   model on its next save: LF→CRLF, multi-line measures collapsed to one line, `lineageTag`s
   rewritten, schema versions bumped. (This is what makes the `Edit` tool fail with "String
   to replace not found" mid-session.) Scripts read the file **fresh at run time** and are
   **CRLF-preserving** (`nl = "\r\n" if "\r\n" in raw else "\n"`), so they survive it.

3. **Idempotent = a clobber costs a re-run, not an afternoon.** The work is encoded *in the
   script*, not in an edit you'd have to reconstruct from memory. Guards like
   `if "'Product Target'" in raw: skip` make every script safe to replay. If Desktop wipes
   something, you just run the script again.

4. **The offline CLI lags Desktop's schemas.** Desktop writes `pagesMetadata/1.1.0`; the
   bundled `pbir` CLI only knows `1.0.0` and false-errors on the newer one. Scripts pin
   `meta["$schema"] = SCHEMA_PAGES` back to `1.0.0` every run so `pbir validate` stays clean.

5. **Harvest-and-relay beats authoring from scratch.** The native gallery doesn't invent
   visual bodies — it deep-copies known-good ones already in the report (preferring `Demo-*`
   pages) and swaps only `name` + `position`, so every role binding stays valid.

**The discipline they ask of you:** run from `projects/test/` with **Desktop closed**, then reopen.

## Script index

| Script | Builds | Notes |
|---|---|---|
| `_build-native-gallery.py` | 6 pages, one of each native `visualType` | **DESTRUCTIVE** — deletes ALL pages first; rebuild the rest after. Harvests + relays existing visuals. |
| `_build-svg-gallery.py` | 2 SVG micro-chart pages (`tableEx`, `dataCategory=ImageUrl`) | Idempotent splice of `_svg-measures.fragment` into `_Measures.tmdl`; appends pages. |
| `_build-pareto.py` | Pareto-Test page | Base recipe — pure **visual calculations** (`RUNNINGSUM`). |
| `_build-pareto-model.py` | Pareto-Model-Test page | Model-measure variant + `# Products to 80%` card. Needs the 5 Pareto measures in `_Measures.tmdl`. |
| `_build-avt.py` | AvT-Variance-Test page | actual-vs-target-variance recipe. Needs AvT measures, `MonthKey` column, `compatibilityLevel 1601`, Month Name `sortByColumn`. |
| `_build-showcase.py` | Recipe-Showcase page | 2×2 grid of all 4 disconnected-selection-emphasis variants. Writes only the visuals — `page.json` + the `pages.json` entry must be added by hand. |
| `_svg-measures.fragment` | — | TMDL fragment (10 SVG measures) spliced by `_build-svg-gallery.py`. Not a script. |

### Full rebuild order (after a wipe)

```text
python _build-native-gallery.py     # DESTRUCTIVE — run first, deletes everything
python _build-svg-gallery.py
python _build-pareto.py
python _build-pareto-model.py
python _build-avt.py
python _build-showcase.py
```

Then `pbir validate "test.Report"` and reopen `test.pbip` in Desktop.
