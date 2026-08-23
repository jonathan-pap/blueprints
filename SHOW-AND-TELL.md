---
marp: true
theme: default
paginate: true
size: 16:9
style: |
  section { font-size: 40px; padding: 60px 80px; }
  h1 { font-size: 96px; line-height: 1.05; }
  h2 { font-size: 72px; }
  h3 { font-size: 48px; }
  .accent { color: #E8662F; }
  .muted { color: #6E7A9C; }
  .big { font-size: 120px; font-weight: 700; line-height: 1; }
  table { font-size: 34px; }
  code { font-size: 34px; }
  pre { font-size: 30px; line-height: 1.25; }
---

<!--
SHOW & TELL — "The folder is the app"
Framework: Myth > Reality  (Myth · Reality check · Concrete example · What's great · DEMO · Where next)
Length: 15–20 min.  Slides carry <20 words; the TALK is in these notes.
Layout rules honoured: body 40px+, titles 72–120px, minimal text, one idea per slide.
Builds/animations: where a note says "BUILD", reveal the lines one at a time in PowerPoint.

RUN OF SHOW (target 17 min)
  0:00  1–2   Title + Myth                         2 min
  2:00  3–4   Reality check (the PDF)              3 min
  5:00  5–7   Concrete example (our workspace)     3 min
  8:00  8–10  What's great                         2 min
 10:00  11    DEMO (live)                           6 min   ← the heart; rehearse it
 16:00  12–13 Where next + close                   1–2 min

Reference: "Stop Building AI Agents. Use This Folder System Instead"
  → bundled PDF: power-bi/_examples/AI_Folder_Architecture.pdf
  → video: https://www.youtube.com/watch?v=MkN-ss2Nl10
Repo: https://github.com/jonathan-pap/blueprints
-->

# The folder <span class="accent">is</span> the app

### Getting AI to do real Power BI work — without building an agent

<!--
Open: "I'm going to show you a system where Claude builds Power BI reports, generates
the data for them, and checks its own work on screen — and there is no agent in it.
It's a folder. That's the whole trick, and it comes from a PDF I'll show you in a minute."
-->

---

## <span class="accent">Myth</span>

# "To make AI do real work, you need an **agent**."

<!--
The common belief. Agents, skill bundles, orchestration frameworks, prompt chains.
Every vendor pitch says the same thing: build an agent, wire tools, add a planner.
Ask the room: who has tried? What happened? (Usually: brittle, expensive, opaque.)
The fear underneath: "if I don't build an agent I'm falling behind."
-->

---

## <span class="accent">Reality check</span>

# Stop building AI agents.
# Use a **folder system** instead.

<span class="muted">— the PDF behind this workspace (3-Layer Folder Architecture)</span>

<!--
This is the title of the PDF bundled in the repo (power-bi/_examples/AI_Folder_Architecture.pdf,
from the YouTube talk). Its argument in one line: a skill bundle loads a 10–25 KB SKILL.md into
context every time it fires — and most of that is irrelevant to the task at hand.
Replace the agent with a folder the model NAVIGATES: load the map, enter one room, open one file.
-->

---

## The three layers

| | Role | Loads when | Size |
|---|---|---|---|
| **L1 Map** | `CLAUDE.md` routes intent → room | always | 3–15 KB |
| **L2 Rooms** | numbered folders, a `context.md` each | on entering | 1–3 KB |
| **L3 Atoms** | one markdown per task | only that task | ≤2 KB |

<!--
BUILD row by row.
L1: tiny router, always loaded — which room?
L2: the room's doctrine — how we think here, what's preferred, the hard rules.
L3: the atom — "add a KPI card", "rename a page". ≤80 lines. Loaded only when that exact task runs.
Five principles in the PDF: the folder is the app · one concern per file · surgical loading ·
workflow over agent · file names are the index (no vector store, the tree IS the lookup).
-->

---

## <span class="accent">Concrete example</span> — our workspace

```text
Workspace-Blueprint/
├── CLAUDE.md          ← L1: which blueprint?
├── power-bi/          ← reports · models · themes · visuals
├── synthetic-data/    ← config-driven star generator
├── tabular-editor/    ← C# scripts · BPA rules
└── briefs/            ← the intake hub
```

<!--
Three blueprints, one hub. Each blueprint is self-contained — zip it, drop it elsewhere, it works.
Point at power-bi: that's the big one — ~570 atomic docs. Then synthetic-data: declare a star
schema in YAML, the engine generates it so totals reconcile at every grain. Tabular-editor: the
model-side toolkit. briefs/: templates + filled examples — where every job starts.
-->

---

## Inside a blueprint: rooms in **pipeline order**

<div class="big">01 → 02 → 03 → 04</div>

### brief → build → bind → review

<!--
Numbered rooms = the workflow. Brief (what do we need), build (edit on disk: PBIR, TMDL, theme),
bind (the live model: MCP, PowerShell, the Desktop bridge), review (validate, audit, lineage).
The numbering isn't decoration — it's sequencing the agent framework would otherwise have to
encode in code. Here the directory tree encodes it.
-->

---

## One room, three kinds of file

| `context.md` | **doctrine** — how to think here |
|---|---|
| `_index.md` | **catalogue** — which file to open |
| `add-kpi-card.md` | **one task** — the exact procedure |

<!--
BUILD row by row. This is the pattern everywhere: 24 rooms, 46 indexes, 573 atoms.
Example from 03-bind/context.md: "three-tier preference — on-disk TMDL, then the MCP, then
PowerShell, and if none reachable: don't guess, ask for a Model Context Brief."
That's a decision rule. It lives in markdown, not in a planner.
-->

---

## <span class="accent">What's great</span> · 1

<div class="big">49 lines</div>

### median atomic file · ~1.7 KB · loaded only when needed

<!--
Surgical loading, measured on our repo: 573 room docs, median 49 lines / 1.7 KB.
Routers 6–13 KB. The PDF's cost argument: five mixed tasks in one session ≈ 100 KB of
SKILL.md vs ≈ 48 KB atomic — roughly half the input tokens per session.
And it compounds: what isn't loaded can't confuse the model.
-->

---

## <span class="accent">What's great</span> · 2

# Markdown **decides.** Code **computes.**

<span class="muted">pbir CLI · Modeling MCP · Desktop Bridge · the data engine — tools, not agents</span>

<!--
The line that keeps this honest. The scripts that exist do mechanical work: resolve a grid to
pixels, splice TMDL, rake a dataset so it reconciles, screenshot a page. None of them decide
what to build next. The sequence is a checklist in markdown (build-report.md: one line per
step + the file to load). Test: could a person run the workflow by hand with just the markdown?
Yes — slower.
-->

---

## <span class="accent">What's great</span> · 3

# `git clone` · `setup.ps1` · done

### zero `SKILL.md` · no plugin · no harness lock-in

<!--
Redistributable: clone, run setup (installs the CLI, Node, the bridge), the MCP config is in
the repo. Count of SKILL.md files outside the provenance folder: zero.
Last week I audited drift against the PDF's rules — the spine held; the one real drift was
reusable code creeping into project folders, and we moved it back into a room. That's the
only thing to police.
-->

---

## <span class="accent">DEMO</span>

# brief → data → model → report → **Claude sees it**

<!--
LIVE, ~6 min. Rehearse. Order:
1. Show the two briefs (synthetic-data/projects/quest-ledger/brief.md,
   power-bi/projects/demo/brief.md) — "the spec is a file".
2. Run the generator + reconcile: python 03-generate/generate.py … / 05-review/reconcile.py …
   → "ALL RECONCILED": declared shares hold at every grain. 40K quests in ~1 s.
3. Hand-off: handoff_to_pbi.py → tables appear in the blank demo model.
4. Say "build the demo" → Claude opens Desktop through the bridge, builds a page, reloads,
   SCREENSHOTS it, reads the PNG, fixes, next page. That's the agent-less self-verify loop.
Fallback if live fails: next slide.
-->

---

## If the demo gods are unkind

<span class="muted">(rendered page from the build — screenshot placeholder)</span>

![bg right:55% contain](power-bi/outputs/demo-guild-overview.png)

<!--
Pre-capture a page with: powerbi-desktop screenshot <pageId> --output power-bi/outputs/demo-guild-overview.png
Talk over it: this PNG was captured by Claude itself through the Desktop Bridge and read back
before it moved to the next page.
-->

---

## <span class="accent">Where next</span>

- Fabric publish from the same folder
- more domains in the data engine
- keep rooms for knowledge, projects for data

<!--
BUILD line by line.
1. Publishing to Fabric is the one gap (parked).
2. The generator is config-only — retail, telecom, fantasy so far; finance / web next.
3. The guardrail: the day reusable logic lands in a project folder instead of a room, it starts
   becoming an agent again. We audit for that.
-->

---

# No agent.
# <span class="accent">A folder.</span>

### github.com/jonathan-pap/blueprints · PDF: `power-bi/_examples/AI_Folder_Architecture.pdf`

<!--
Close on the myth: you don't need an agent to get real work out of AI. You need a map, rooms,
and atoms — and the discipline to keep knowledge in markdown.
Invite: clone it, run setup, say "build the demo".
Questions.
-->
