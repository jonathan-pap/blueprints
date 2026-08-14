# Handoff — generate the wireframe *outside* this blueprint

The text wireframe + `story.md` are **tool-agnostic**, so you can turn them into a real visual elsewhere —
a Claude HTML/SVG mockup, a **Figma** design, or whatever a design AI accepts. The trick is to emit a
**portable spec** (structured, not ASCII art) that tools consume without parsing boxes.

## The portable spec (the interchange format)

Alongside the ASCII, produce a structured spec — one object per page, zones with positions, placeholders
typed. This is the single source every target reads.

```jsonc
{
  "canvas": { "w": 1280, "h": 720, "margin": 24, "grid": 8 },
  "pages": [
    {
      "name": "Executive Summary",
      "question": "Are we up or down vs plan, and where's the gap?",
      "zones": [
        { "zone": "header",     "x": 24,  "y": 24,  "w": 1232, "h": 40,
          "items": [ { "type": "title", "label": "Sales Performance — FY26" },
                     { "type": "text", "label": "Updated {date}" } ] },
        { "zone": "filterRail", "x": 24,  "y": 80,  "w": 232,  "h": 616,
          "items": [ { "type": "slicer", "label": "Date" }, { "type": "slicer", "label": "Region" } ] },
        { "zone": "kpiRow",     "x": 272, "y": 80,  "w": 984,  "h": 120,
          "items": [ { "type": "kpi", "label": "Total Sales" }, { "type": "kpi", "label": "Margin %" },
                     { "type": "kpi", "label": "vs Target" },   { "type": "kpi", "label": "YoY %" } ] },
        { "zone": "main",       "x": 272, "y": 216, "w": 640,  "h": 320, "hero": true,
          "items": [ { "type": "bar", "label": "Sales vs Target by Region" } ] },
        { "zone": "main",       "x": 928, "y": 216, "w": 328,  "h": 320,
          "items": [ { "type": "line", "label": "Sales trend" } ] },
        { "zone": "detail",     "x": 272, "y": 552, "w": 984,  "h": 144,
          "items": [ { "type": "table", "label": "Region · Sales · Target · Δ · YoY" } ] }
      ]
    }
  ]
}
```

`type` is the placeholder **intent** (`kpi/card/bar/line/donut/map/table/slicer/title/text`); it maps to a
real visual at build (`../../02-build/report/references/visual-cookbook.md`) and to a shape in a design tool.
Prompt **E** in [`prompts.md`](prompts.md) emits this from an approved wireframe.

## Targets

| Target | How | You get |
|---|---|---|
| **Claude / any LLM** | prompt below → an **HTML or SVG artifact** | greyscale, interactive-ish mockup you can share |
| **Figma** | Figma MCP / connector (if available) → generate frames from the spec | editable design frames, one per page |
| **Any design AI** | hand it the spec + `story.md` | varies by tool |

### → Claude → HTML/SVG mockup (works anywhere)

```
Render this wireframe spec as ONE self-contained greyscale HTML mockup, 1280×720 per page.
Rules: boxes + labels only, NO colour, NO real data, NO brand styling. Each zone a bordered
block positioned by its x/y/w/h; the hero item larger/heavier; label every placeholder with
its type + label. Theme-agnostic. Output an artifact.
<paste the portable spec>
```

This is the cheapest "real picture" for sign-off — publish it as an Artifact and share the link.

### → Figma (via a Figma MCP / connector)

If a Figma MCP or connector is wired up (not part of this blueprint — it's your agent's setup):

1. Load the Figma design skill (e.g. `/figma-generate-design`) — it's mandatory before generating.
2. Hand it **`story.md` + the portable spec**. Ask for **one frame per page at 1280×720**, each zone an
   **auto-layout container**, each placeholder a **labeled rectangle** named `type: label`. Greyscale, low-fi.
3. Iterate in Figma; the spec stays the source of truth here.

No Figma MCP? Paste the spec into **Figma's own AI / FigJam**, or generate the HTML mock above and rebuild
it in Figma manually.

### → generic design AI

Give it two files: **`story.md`** (arc + page purposes, so it understands *why*) and the **portable spec**
(pages → zones → placeholders, so it knows *what/where*). Ask for low-fi, greyscale frames.

## Round-trip

After the report is built, screenshot the real pages via the Desktop Bridge
(`../../03-bind/desktop-bridge.md`) and compare against the mockup — same zones, now with real data + theme.
The wireframe spec is what keeps design tool, blueprint, and built report describing the *same* layout.
