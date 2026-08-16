# Design system — project layout tokens

> The layout counterpart to the theme. The **theme** governs appearance (colors, fonts, padding) and
> ships inside the `.pbip` — Power BI reads it at render time. **`design-system.yaml`** governs
> *dimensions* (size, position, grid, gaps) and is read by **Claude at build time** — Power BI never
> sees it. It's the level the theme cascade can't reach, because the theme JSON schema has no
> `width`/`height`/`x`/`y`.

## Why it exists

Power BI themes cannot set size or position. Without a tokens file, every `pbir add visual` call is
free to choose its own dimensions, so visuals of the same type drift (e.g. seven different slicer
sizes across one report). `design-system.yaml` closes that gap: it's the single source of truth for
dimensions, read before generation and checked after.

## Where it lives

```text
projects/<name>/design-system.yaml      # this project's tokens
```

Start from the copyable template next to this file: [design-system-default.yaml](design-system-default.yaml).

## The rule (mirrors theme-first)

**A visual's size and position come from `design-system.yaml` by default.** Apply a per-visual
override only when the brief explicitly asks for that visual, or it's a genuine one-off — and record
the reason in the `overrides:` block so the audit hook knows it's intentional. Same discipline as
theme-first, second axis.

## Workflow — read before every add

1. Open `projects/<name>/design-system.yaml`.
2. Map the requested visual to a **span** (or a region template):
   - "year slicer" → `defaults.slicer` → span `[2,1]`, band `summary`.
   - "KPI row" → `layouts.kpi_row_4` → four card regions `[1,1,4,4] … [10,1,13,4]`.
3. **Resolve span/region → pixels** with the cell math in [layout-guidelines.md](layout-guidelines.md):
   on 1280×720, span `[2,1]` → 192×41; region `[1,1,4,4]` → 296×155 at x24 y24.
4. Emit the `pbir` command with the resolved numbers:
   ```bash
   pbir add visual slicer "<...>.Report/Market Overview.Page" --title "Year" \
     --x 24 --y 24 --width 192 --height 41
   ```

Spans/regions are decided once in the yaml and **resolve per canvas** — no restating dimensions per
request, and the same contract renders on 720p or 1080p.

## Token reference

| Key | Meaning |
|---|---|
| `meta.page` | page size; **cell size derives from it** (query before placing — [page-dimensions.md](page-dimensions.md)) |
| `meta.theme` | the theme that owns appearance (this file owns only dimensions) |
| `grid` | the **12×12 grid**: `columns`/`rows`/`gutter`/`margin`/`snap` — cell math in [layout-guidelines.md](layout-guidelines.md) |
| `bands` | detail-gradient **row bands** ([detail-gradient.md](detail-gradient.md)) — a semantic label on rows, not geometry |
| `defaults.<type>` | per-type default **span** `[cols,rows]` (+ `band:` hint, `type:` pin for slicers) |
| `layouts.<name>` | named multi-visual **region templates** — `[col,row,col,row]` rectangles |
| `pages` | the report's pages and which tokens/regions each uses |
| `overrides` | intentional deviations, with a reason (the audit hook treats these as allowed) |

## Enforcement is two-tier

Same pattern the blueprint uses for field binding:

| | Soft (Claude follows) | Hard (hook catches) |
|---|---|---|
| **Binding** | check canonical names ([bind/find-canonical-name.md](../bind/find-canonical-name.md)) | `validate-visual-binding.sh` |
| **Layout** | this file's "read tokens first" rule | [`audit-layout-consistency.sh`](../../../04-review/hooks/audit-layout-consistency.sh) — flags off-token sizes, off-grid + sub-pixel positions |

The generator and the auditor read the **same yaml**, so the rule that builds visuals can't drift
from the rule that checks them.

## Relationship to the theme

- Need a **color / font / padding** change → that's the theme ([../../theme/context.md](../../theme/context.md)).
- Need a **size / position / spacing** change → that's this file.
- A property on >2 visuals of one type → promote it (theme override for appearance; a new
  `defaults.<type>` entry for dimensions).

## Related

- [layout-guidelines.md](layout-guidelines.md) — the equal-gap math the `layouts:` block encodes
- [size-visual.md](size-visual.md) · [position-visual.md](position-visual.md) — the CLI the tokens feed
- [detail-gradient.md](detail-gradient.md) — the zones model
