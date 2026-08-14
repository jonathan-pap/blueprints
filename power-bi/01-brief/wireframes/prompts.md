# Prompts — drive the AI through story + wireframe

Copy-paste prompts for each phase of [`workflow.md`](workflow.md). Paste your filled
[`brief-template.md`](brief-template.md) (or the report brief) where indicated. They chain: A → B (per page)
→ C → D. Keep the AI **low-fi** — boxes and labels, not styling.

---

## A · Derive the story arc

```
You are planning a Power BI report. Here is the brief:
<paste the Wireframe & Story Brief>

Produce a DATA STORY, not a list of charts:
1. State the ONE decision this report drives (one sentence).
2. List the audience's questions in the order they'd ask them.
3. Choose a narrative arc (Overview→Analysis→Detail | Martini glass | Drill path) and justify it in one line.
4. Output an ORDERED PAGE LIST. For each page:
   - Page name
   - The single question it answers
   - The "so what" (the takeaway a reader leaves with)
   - The 3–6 KPIs/visual *intents* it needs (intent, not final chart type)
Keep it to <N> pages. Flag any question the brief's data can't answer.
```

## B · Wireframe one page

```
Wireframe page "<PAGE NAME>" from the story. Canvas 1280×720, 24px margins.
Use the notation in notation.md: draw the page as an ASCII grid of ZONES
(header / KPI row / main / detail / filter rail), and place PLACEHOLDER visuals as
[Type ▸ label] (e.g. [KPI: Total Sales], [Bar ▸ Sales by Region], [Slicer: Date]).

Rules:
- Low-fi only: boxes + labels, NO colors, NO real data, NO final styling.
- One HERO visual (biggest, top-left-ish) = the page's answer.
- 4–6 visuals for an analysis page; fewer + bigger for a summary.
- State the reading order (Z or F) and why the hero is the hero.
- Only use fields/measures that exist (per the Model Context Brief); flag any that don't.
Output: the ASCII wireframe + a 2-line rationale.
```

## C · Critique the wireframe (against the brief)

```
Critique this wireframe against the brief. Be specific and cut ruthlessly.
<paste the wireframe(s) + the brief>

Check:
- ANSWERS: does each page answer its assigned question? Anything decorative → cut. Anything missing → add.
- FLOW: does page order match the arc? Any page to merge or drop?
- BALANCE: over-full pages (split), under-full (merge), repeated visuals (consolidate).
- HERO & ORDER: is there one clear hero and a sane reading order per page?
- FEASIBILITY: every placeholder maps to a visual the model can feed?
Return a revised page list + revised wireframes, and a short list of what you changed and why.
```

## D · Convert the approved wireframe to a build plan

```
The wireframe is approved. Turn it into a build plan for the 02-build room.
For each page and each placeholder visual:
- Pick the concrete Power BI visual type (use the visual-cookbook rules).
- Give position + size on the 1280×720 canvas as design-system.yaml zones/tokens.
- Bind it to the real measure/field (canonical names — verify, don't guess).
Output: a per-page table [visual | type | fields | x/y/w/h | zone], ready for pbir add visual.
Also save the story (arc + page purposes) to projects/<name>/story.md.
```

---

## Tips

- **Feed the model reality.** If the model exists, attach the
  [Model Context Brief](../../../briefs/model-context-brief.md) so placeholders bind to real fields.
- **Iterate on text, not PBIR.** Re-run B/C until the wireframe is agreed — changing an ASCII box is free;
  changing a built page is not.
- **Stakeholder mockup (optional).** Ask for the approved wireframe as an HTML/SVG artifact for sign-off —
  same zones, still no real data.
- **After build, compare.** Screenshot the built pages via the Desktop Bridge
  (`../../03-bind/desktop-bridge.md`) and check them back against the wireframe.
