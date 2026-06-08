# Tokens

Placeholders to substitute into the templates before applying. Gathered during the Phase 1
intake (see [workflow.md](workflow.md)).

## Required (always)

| Token | What | Example |
|---|---|---|
| `<PREFIX>` | Stable prefix for all recipe-generated measures so they sort together in the display folder. Short. | `Funnel`, `WF`, `Bridge`, `Attrition` |
| `<STEPS_TABLE>` | Disconnected helper table name. Convention: `<PREFIX>Steps` (PascalCase, no spaces). | `FunnelSteps`, `WaterfallSteps`, `BridgeSteps` |
| `<MEASURE_TABLE>` | The central measures table — usually a hidden `_Measures` calculated table the workspace already has. | `_Measures` |
| `<DISPLAY_FOLDER>` | Display folder for the recipe's measures inside `<MEASURE_TABLE>`. | `16. Waterfall Funnel`, `9. Variance Bridge` |
| `<STEPS>` | Ordered list of step definitions, gathered in Q1. Each: name, type (total/drop), source measure. Length N. | `[("Total Volume", "total", "[Trade Quantity]"), ("NPC Mediated", "drop", "[NPC Volume]"), ...]` |
| `<PAGE_ID>` | The report page name (filesystem-safe). | `waterfall`, `funnel-test`, `revenue-bridge` |
| `<PAGE_DISPLAY_NAME>` | Human-friendly page title. | `Revenue Bridge YoY`, `Pipeline Funnel` |
| `<VISUAL_NAME>` | Visual ID inside the page folder. | `waterfall-001`, `bridge-vis` |

## Required (variant-specific)

| Token | When needed | What |
|---|---|---|
| `<ORIENTATION>` | always | `vertical` or `horizontal` (gathered Q3) |
| `<LABEL_STYLE>` | always | `standard` or `detailed` (gathered Q3) |
| `<FIRST_TOTAL_MEASURE>` | always | The source measure for the first TOTAL step in `<STEPS>`. Used by `<PREFIX> Axis Max` and `<PREFIX> Label Anchor`. |
| `<AXIS_MAX_HEADROOM>` | always | Multiplier for axis padding above the first total. Default `1.15` (15% headroom). |
| `<AXIS_MAX_ROUND>` | always | Round-up unit for the axis max. Default depends on scale: `10` for hundreds, `1000` for thousands+, `1000000` for millions+. |
| `<STACKED_STEPS>` | if Q2 = yes | List of `(step_name, [(segment_name, source_measure), ...])` for steps that split into sub-segments. Gathered Q2a. |

## Color tokens (palette — typically defaults work)

| Token | What | Default |
|---|---|---|
| `<COLOR_TOTAL_START>` | Color for the start-total bar (Step 1). | `#1F3A5F` (navy) |
| `<COLOR_TOTAL_INTERMEDIATE>` | Color for intermediate total bars. | `#7AAE89` (soft green) |
| `<COLOR_TOTAL_END>` | Color for the end-total bar. | `#2D6948` (dark green) |
| `<COLOR_DROP_FIRST>` | Color for the first drop. | `#CE5A4E` (coral) |
| `<COLOR_DROP_SECOND>` | Color for subsequent drops. | `#A23A2A` (darker red) |
| `<COLOR_TIER_LOW>` | For stacked variant, low-tier segment color. | `#E0A030` (warm orange) |
| `<COLOR_TIER_MID>` | For stacked variant, mid-tier segment color. | `#7AAE89` (soft green) |
| `<COLOR_TIER_HIGH>` | For stacked variant, high-tier segment color. | `#2D6948` (dark green) |

**Recommendation:** for stacked variants, use **tier-coherent colors** — the same color for a
given tier wherever it appears (in the composition stack AND in the corresponding drop bar).
Reads as "where did the orange go" across the funnel.

## Generated names (deterministic from above)

These don't need to be asked — derived from `<PREFIX>` and `<STEPS>`:

| Generated | Pattern |
|---|---|
| Floater | `<PREFIX> Base` |
| Per-step body | `<PREFIX> Body · <Step name>` |
| Simple label | `<PREFIX> Label` |
| Rich label | `<PREFIX> Label (rich)` |
| Y2 anchor | `<PREFIX> Label Anchor` |
| Axis max | `<PREFIX> Axis Max` |
| Horizontal pad (horizontal only) | `<PREFIX> Label Pad` |
| Stacked sub-segments (stacked only) | `<PREFIX> Stack · <Step name> · <Segment name>` |

## Lineage tags

The MCP auto-generates these on create. If pasting into Tabular Editor manually, use
[`../../model/object-types/lineage-tag.md`](../../model/object-types/lineage-tag.md) — every
new object needs a fresh GUID. The recipe templates leave `lineageTag:` lines blank so the
tool fills them in.

## Defaults summary

If the user skips Q3 (orientation + label style), default to:
- `<ORIENTATION>` = `vertical`
- `<LABEL_STYLE>` = `standard`

These give the simplest readable result and are the most-tested combination.
