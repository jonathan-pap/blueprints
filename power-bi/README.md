# Power BI Desktop Workspace Blueprint

A reusable workspace for working on Power BI Desktop projects (PBIP format) with Claude or any other LLM that can read folders. Built on the 3-Layer Folder Architecture: a top-level map, rooms that load only when needed, and references that load only when a room asks.

## Quick start

1. Copy this `power-bi/` folder into a new working directory.
2. Point Claude (or your agent) at the directory and tell it to read [CLAUDE.md](CLAUDE.md).
3. Start a project: `mkdir projects/<my-project>` then follow [projects/README.md](projects/README.md).
4. The agent will pick the right room from `CLAUDE.md`'s routing table based on what you ask for.

## Folder map

```
power-bi/
├── CLAUDE.md          ← Layer 1: master router (always loaded)
├── 01-brief/          ← Layer 2: discovery, KPIs, layout decisions
├── 02-build/          ← Layer 2: edit report / model / theme / custom visuals
│   ├── report/
│   ├── model/
│   ├── theme/
│   └── visuals/
│       ├── deneb/   svg/   python/   r/
├── 03-bind/           ← Layer 2: live model bridge (TOM + ADOMD via PowerShell)
├── 04-review/         ← Layer 2: validate, audit, performance, hooks
├── projects/          ← raw layer: actual PBI projects you're editing
└── outputs/           ← output layer: dated generated artifacts
```

Each room has a slim `context.md` that lists which `references/<topic>.md` to load for a given task. The references are the bulk of the knowledge — loaded only on demand.

## Workflow at a glance

| User intent | Rooms loaded | Live model? |
|---|---|---|
| "Build me a sales dashboard" | `01-brief/` → `02-build/report/` | No |
| "Add a KPI card" | `02-build/report/` | No |
| "Bind this card to [Total Revenue]" | `03-bind/` (one-shot) + `02-build/report/` | Yes (briefly) |
| "Change the theme colors" | `02-build/theme/` | No |
| "Add a measure to the model" | `02-build/model/` (TMDL) or `03-bind/` (TOM, live) | Optional |
| "Build a custom sparkline in the table" | `02-build/visuals/svg/` | No |
| "Audit the sales report" | `04-review/` | No |

The full routing table is in [CLAUDE.md](CLAUDE.md).

## Reuse for any project

Three properties make this reusable:

1. **Self-contained.** Everything the agent needs is inside `power-bi/`. No external dependencies beyond the `pbir` CLI and (for `03-bind/`) PowerShell + TOM.
2. **Pipeline-shaped.** Rooms are numbered to enforce order; the structure mirrors the actual PBI lifecycle.
3. **Naming convention enforces routing.** Folders are kebab-case, outputs are dated, projects follow the PBIP suffix convention. The agent navigates by name, not memorized paths.

## Required tooling

| Tool | Purpose | Install |
|---|---|---|
| `pbir` CLI | All `02-build/report/` mutations | `uv tool install pbir-cli` or `pip install pbir-cli` |
| `jq` | JSON validation (used by hooks) | Platform package manager |
| PowerShell 7+ | `03-bind/` scripts | Pre-installed on Windows; via Parallels on macOS |
| NuGet | TOM / ADOMD.NET packages for `03-bind/` | `winget install Microsoft.NuGet` |
| Power BI Desktop | The target tool | Microsoft Store or direct download |

Tools install on first use (`03-bind/` quickstart triggers the NuGet packages). Nothing here requires a Fabric license or service connection — work is done locally against `.pbip` files and Desktop.

## What's in `_examples/`

Upstream reference snapshot used to derive the atomic files. **Do not load unless explicitly asked.** The rooms here were atomized from those references to fit the 3-Layer architecture (PDF: `_examples/AI_Folder_Architecture.pdf`).

## License

Reference content derives from upstream community plugins (GPL-3.0). Routing and structure (this blueprint) is yours to adapt.
