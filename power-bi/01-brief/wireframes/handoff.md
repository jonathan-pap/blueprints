# Handoff — generate the wireframe *outside* this blueprint

The text wireframe + `story.md` are **tool-agnostic**, so you can turn them into a real visual elsewhere —
a Claude HTML/SVG mockup, a **Figma** design, or whatever a design AI accepts. The trick is to emit a
**portable spec** (structured, not ASCII art) that tools consume without parsing boxes.

## The portable spec (the interchange format)

Alongside the ASCII, produce a structured spec — one object per page, placements typed and positioned by
**grid region**. This is the single source every target reads. Geometry is the **12×12 grid** (same as the
build), so the spec is resolution-independent and drops straight into a
[design contract](../../02-build/report/layout/design-contract.md) `layout_contract`.

```jsonc
{
  "canvas": { "w": 1280, "h": 720, "margin": 24, "gutter": 16, "grid": { "columns": 12, "rows": 12 } },
  "pages": [
    {
      "name": "Executive Summary",
      "question": "Are we up or down vs plan, and where's the gap?",
      // placements: each has a grid `region` [col_start,row_start,col_end,row_end]
      // (1-indexed, END-EXCLUSIVE) + a `band` (summary|analysis|detail) + typed `items`.
      // Pixel x/y/w/h are OPTIONAL — derive them from the region for tools that want absolute coords.
      "placements": [
        { "band": "summary",  "region": [1, 1, 13, 2],
          "items": [ { "type": "title", "label": "Sales Performance — FY26" },
                     { "type": "text", "label": "Updated {date}" } ] },
        { "band": "summary",  "region": [1, 1, 3, 13],
          "items": [ { "type": "slicer", "label": "Date" }, { "type": "slicer", "label": "Region" } ] },
        { "band": "summary",  "region": [3, 2, 13, 4], "token": "layouts.kpi_row_4",
          "items": [ { "type": "kpi", "label": "Total Sales" }, { "type": "kpi", "label": "Margin %" },
                     { "type": "kpi", "label": "vs Target" },   { "type": "kpi", "label": "YoY %" } ] },
        { "band": "analysis", "region": [3, 4, 9, 10], "hero": true,
          "items": [ { "type": "bar", "label": "Sales vs Target by Region" } ] },
        { "band": "analysis", "region": [9, 4, 13, 10],
          "items": [ { "type": "line", "label": "Sales trend" } ] },
        { "band": "detail",   "region": [3, 10, 13, 13],
          "items": [ { "type": "table", "label": "Region · Sales · Target · Δ · YoY" } ] }
      ]
    }
  ]
}
```

`region` is the grid rectangle (resolve to pixels with the
[cell math](../../02-build/report/layout/layout-guidelines.md#grid-12x12)); `band` is the semantic
detail-gradient row label; `token` optionally names a `design-system.yaml` span/template. `type` is the
placeholder **intent** (`kpi/card/bar/line/donut/map/table/slicer/title/text`); it maps to a real visual at
build (`../../02-build/report/references/visual-cookbook.md`) and to a shape in a design tool. Prompt **E**
in [`prompts.md`](prompts.md) emits this from an approved wireframe — because it already carries regions +
bands, each `placement` becomes a `layout_contract` placement one-to-one.

## Targets

| Target | How | You get |
|---|---|---|
| **Claude / any LLM** | prompt below → an **HTML or SVG artifact** | greyscale, interactive-ish mockup you can share |
| **Figma** | Figma MCP / connector (if available) → generate frames from the spec | editable design frames, one per page |
| **Any design AI** | hand it the spec + `story.md` | varies by tool |

### → Claude → HTML/SVG mockup (works anywhere)

```
Render this wireframe spec as ONE self-contained greyscale HTML mockup, 1280×720 per page.
The spec places every block on a 12×12 grid: resolve each `region` [c1,r1,c2,r2] (1-indexed,
end-exclusive) to pixels — colW=(1280−2·24−16·11)/12, rowH=(720−2·24−16·11)/12, margin 24,
gutter 16 — and draw a bordered block there. Boxes + labels only, NO colour, NO real data, NO
brand styling; the `hero` item larger/heavier; label every placeholder with its type + label.
Theme-agnostic. Output an artifact.
<paste the portable spec>
```

This is the cheapest "real picture" for sign-off — publish it as an Artifact and share the link.

### → Figma (via a Figma MCP / connector)

If a Figma MCP or connector is wired up (not part of this blueprint — it's your agent's setup):

1. Load the Figma design skill (e.g. `/figma-generate-design`) — it's mandatory before generating.
2. Hand it **`story.md` + the portable spec**. Ask for **one frame per page at 1280×720** on a **12-column
   layout grid**, each placement an **auto-layout container** at its `region`, each placeholder a
   **labeled rectangle** named `type: label`. Greyscale, low-fi.
3. Iterate in Figma; the spec stays the source of truth here.

No Figma MCP? Paste the spec into **Figma's own AI / FigJam**, or generate the HTML mock above and rebuild
it in Figma manually.

### → generic design AI

Give it two files: **`story.md`** (arc + page purposes, so it understands *why*) and the **portable spec**
(pages → grid placements → placeholders, so it knows *what/where*). Ask for low-fi, greyscale frames.

## Round-trip

After the report is built, screenshot the real pages via the Desktop Bridge
(`../../03-bind/desktop-bridge.md`) and compare against the mockup — same grid regions, now with real data
+ theme. The wireframe spec is what keeps design tool, blueprint, and built report describing the *same* layout.
