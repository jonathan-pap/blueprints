# Workspace Blueprint

A collection of self-contained **folder-as-app blueprints** for working with various data / BI tools. Each blueprint follows the 3-Layer Folder Architecture: a top-level map, rooms that load only when needed, and atomic step files that load only when their workflow runs.

## How to use

1. Point Claude (or any LLM that can read folders) at this directory.
2. Tell it to read [claude.md](claude.md) — the blueprint directory.
3. Pick the blueprint that matches your task. Claude follows that blueprint's own `claude.md` from there.

## Current blueprints

| Blueprint | Tool | Status |
| --- | --- | --- |
| [power-bi/](power-bi/) | Power BI Desktop (PBIP format) | Complete — 265 atomic files across 11 rooms |
| [synthetic-data/](synthetic-data/) | Synthetic / dummy data creation (Python-first) | Skeleton — 5 rooms + Power BI hand-off; rooms grow per job |

## Why folder-as-app

Each blueprint:

- Loads only the atomic step files needed for the current task (typical: 3–10 KB of context, not 30+ KB)
- Is portable — copy the folder into any project to work alongside it
- Uses no external state — the file system is the database, file names are the index

## Adding a new blueprint

Create a top-level kebab-case folder. Follow the same pattern: `claude.md`, `README.md`, numbered rooms, `projects/`, `outputs/`, `_examples/`. Add a one-line entry to the root `claude.md`'s "Available blueprints" list.

## Architecture reference

For the full walkthrough with workflow diagrams (intent routing, brief-first execution, 3-tier live-model preference, theme creation, hook subsystems) and an atomic-vs-plugin cost comparison, see **[HOW-IT-WORKS.md](HOW-IT-WORKS.md)**.

The 3-Layer Folder Architecture itself is documented in [power-bi/_examples/AI_Folder_Architecture.pdf](power-bi/_examples/AI_Folder_Architecture.pdf). Watch the original video: [Stop Building AI Agents. Use This Folder System Instead](https://www.youtube.com/watch?v=MkN-ss2Nl10).
