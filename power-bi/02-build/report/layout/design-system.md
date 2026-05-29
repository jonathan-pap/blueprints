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
2. Map the requested visual to a token:
   - "year slicer" → `defaults.slicer` → `type: slicer`, `240 × 40`, zone `summary`.
   - "KPI row" → `layouts.kpi_row_4` → four `296 × 130` cards at x `[24, 336, 648, 960]`.
3. Emit the `pbir` command with those exact numbers:
   ```bash
   pbir add visual slicer "<...>.Report/Market Overview.Page" --title "Year" \
     --x 24 --y 24 --width 240 --height 40
   ```
4. Resolve the zone's `y` from `zones.<zone>` unless the layout token already pins `y`.

No restating dimensions per request — they're decided once in the yaml.

## Token reference

| Key | Meaning |
|---|---|
| `meta.page` | page size; every page uses it (query before placing — [page-dimensions.md](page-dimensions.md)) |
| `meta.theme` | the theme that owns appearance (this file owns only dimensions) |
| `grid.unit` / `grid.snap_to` | positions and sizes snap to multiples of these |
| `margins` / `gaps` | equal edge margins + equal gaps — the [layout-guidelines.md](layout-guidelines.md) golden rules |
| `zones` | detail-gradient bands ([detail-gradient.md](detail-gradient.md)); each gives a `y` + `height` |
| `defaults.<type>` | per-visual-type size (+ `type:` pin for slicers, `zone:` hint) |
| `layouts.<name>` | pre-computed multi-visual placements (equal-gap math done once) |
| `pages` | the report's pages and which tokens each uses |
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
