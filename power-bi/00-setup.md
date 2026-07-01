# Setup — tooling & prerequisites

> Read this once per machine before using the blueprint. It explains every external tool the
> rooms assume, **what it is, who makes it, how to install it, and what to do if you can't.**
> Nothing here needs a Fabric license or a cloud connection — all work is local against `.pbip` files.

## New-machine quickstart

**One-shot (Windows / PowerShell)** — [`setup.ps1`](setup.ps1):

```powershell
pwsh ./setup.ps1                  # checks Python, installs/updates pbir CLI, reports jq + Desktop
pwsh ./setup.ps1 -InstallMissing  # ALSO winget-installs Python / jq / Power BI Desktop if absent
```

Default run is **non-destructive** — it only pip-installs `pbir-cli` and reports the rest;
`-InstallMissing` opts into the winget installs. Python deps alone: `pip install -r requirements.txt`.

**Manual equivalent:**

```bash
pip install -U pbir-cli        #  or:  uv tool install pbir-cli      (>= 0.9.25)
pbir --version
python --version               #  3.10+
jq --version                   #  used by 04-review hooks
# + Power BI Desktop (Microsoft Store or direct download)
```

`03-bind/` (live model) additionally needs PowerShell 7+ and the TOM/ADOMD NuGet packages — those
self-install on first use from that room's quickstart. The **Power BI Modeling MCP** (model edits) needs
**Node.js** and is wired via npx or the VS Code extension — see [Power BI Modeling MCP](#power-bi-modeling-mcp-model-mutations).

## The `pbir` CLI — read this before you depend on it

| | |
|---|---|
| **What it is** | A command-line tool that reads/writes the **PBIR** files — the `<project>.Report/definition/` folder (pages, visuals, `pages.json`). It powers `pbir validate`, `add page`, `add visual`, `color`, `fonts`, `tree`, `usage`, `model -d`. Because it works on the files **on disk, it runs headless** (Power BI Desktop closed) — which is exactly this blueprint's "edit on disk, reopen Desktop to view" workflow. |
| **Who makes it** | **Kurt Buhler & Maxim Anatsko** — a **community / third-party** tool. **It is NOT a Microsoft product.** Distributed as a closed-source binary wheel on PyPI as `pbir-cli`. |
| **License** | ⚠️ **Custom Non-Commercial License.** Free for non-commercial use; **commercial use requires written permission** from the authors. If this machine produces commercial work, get permission or use the fallback below. |
| **Version** | The blueprint assumes **≥ 0.9.25** — that release fixed a fatal `add page`/`add visual` write-block and added `validate --semantic`, `color`, `fonts`, `usage`. Upgrade with `pip install -U pbir-cli`. |
| **Package vs command** | The PyPI **package** is `pbir-cli`; the installed **command** is `pbir`. (There is no `pbi_cli` / `pbi-cli` — if you see that written down, it's a typo for `pbir`.) |

### Windows encoding flags

`pbir`'s help and validation output crash on cp1252. Prefix commands with:

```bash
PYTHONIOENCODING=utf-8 PYTHONUTF8=1 COLUMNS=400 pbir validate "<project>.Report"
```

### Why this tool (and what it costs us)

Microsoft documents the **PBIP/PBIR file format** but ships **no official CLI to mutate it**. The
alternatives don't cover headless report editing: Desktop's UI is manual, **Tabular Editor is
model-only**, and `pbi-tools` is `.pbix`-era. `pbir` is the one tool that gives **schema/field/visual
validation + structural report edits** without opening Desktop. It is **convenience, not load-bearing**
— see the fallback.

### Fallback if you won't/can't use `pbir` (e.g. commercial use)

Everything `pbir` does has a documented manual path:

- **Report edits** — hand-author the PBIR JSON under `<project>.Report/definition/` (each visual/page
  is a separate schema-documented JSON file). See `02-build/report/schema-patterns/`.
- **Model edits** — go through the **Power BI Modeling MCP** (Desktop open) or hand-edit TMDL
  (Desktop closed). See `03-bind/` and the MCP-first rule in `02-build/context.md`.
- **Validation** — `jq empty <file>.json` for syntax; open in Desktop to catch binding/schema errors.

## Power BI Modeling MCP (model mutations)

The blueprint is **MCP-first for model edits** — measures, columns, relationships, calc tables go
through the **Power BI Modeling MCP** (Desktop open) rather than hand-editing TMDL. Unlike `pbir`, this
**is an official Microsoft product** ([`microsoft/powerbi-modeling-mcp`](https://github.com/microsoft/powerbi-modeling-mcp)),
distributed on npm as [`@microsoft/powerbi-modeling-mcp`](https://www.npmjs.com/package/@microsoft/powerbi-modeling-mcp).

**Prerequisites:** Node.js 18+ (`winget install OpenJS.NodeJS.LTS`) and Power BI Desktop **open** on the
target model. Two ways to wire it up:

**A. VS Code extension (easiest)** — install GitHub Copilot + Copilot Chat, then the "Power BI Modeling
MCP" extension ([aka.ms/powerbi-modeling-mcp-vscode](https://aka.ms/powerbi-modeling-mcp-vscode)). The
hammer/MCP-tools icon in Copilot Chat should list `powerbi-modeling-mcp`.

**B. Manual stdio config (any MCP client — Claude Code, etc.)** — npx fetches the server on first use:

```jsonc
"powerbi-modeling-mcp": {
  "type": "stdio",
  "command": "npx",
  "args": ["-y", "@microsoft/powerbi-modeling-mcp@latest", "--start"]
}
```

Verify the tools are live, then connect to the running Desktop instance (the MCP exposes
`connection_operations` to list/attach local instances). Docs:
[Power BI MCP servers overview](https://learn.microsoft.com/en-us/power-bi/developer/mcp/mcp-servers-overview).
If the MCP is unavailable, the fallback is hand-editing TMDL with Desktop **closed** (see `03-bind/`).

## Power BI Desktop Bridge (preview — optional, first-party)

A Microsoft **preview** capability: a server **inside Power BI Desktop** that lets an agent **reload the
open report from disk** and **screenshot pages** for visual self-verification — enabling a real-time
edit → `reload` → `screenshot` loop with Desktop staying open. Drive it with the first-party CLI
[`@microsoft/powerbi-desktop-bridge-cli`](https://www.npmjs.com/package/@microsoft/powerbi-desktop-bridge-cli)
(`npm install -g` — auto-installed by `setup.ps1` when Node is present):

```bash
powerbi-desktop open "<path.pbip>"          # launch Desktop with a report
powerbi-desktop status                       # PID + reportDir + page list
powerbi-desktop reload --pid <pid> --wait-seconds 120
powerbi-desktop screenshot <pageId> --pid <pid> --wait-seconds 120 --output page.png
```

Enabled by default in Desktop (*Options → Preview features → "Enable external tool access to Power BI
Desktop through secure local APIs"*). **Opt-in** — gated by `desktop_bridge` in
[`03-bind/via-powershell/hooks/config.yaml`](03-bind/via-powershell/hooks/config.yaml). Full command
loop, `--wait-seconds` timeout fix, and the error table: [`03-bind/desktop-bridge.md`](03-bind/desktop-bridge.md).

## Microsoft reference docs (the *format*, not the CLI)

The file format `pbir` edits is Microsoft-official and publicly documented:

- [Power BI Desktop projects (PBIP) — overview](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-overview)
- [Project report folder (PBIR)](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-report) — the `definition/` structure
- [Enhanced report format (PBIR)](https://learn.microsoft.com/en-us/power-bi/developer/embedded/projects-enhanced-report-format) — why each visual/page is its own JSON with a public schema
- [TMDL — overview](https://learn.microsoft.com/en-us/analysis-services/tmdl/tmdl-overview) — the semantic-model text format edited in `02-build/model/`

## Full tooling matrix

| Tool | Used by | Microsoft? | Install |
|---|---|---|---|
| `pbir` CLI (`pbir-cli`) | All `02-build/report/` + `04-review/` validation | **No** (community, non-commercial license) | `pip install -U pbir-cli` (≥ 0.9.25) |
| Python 3.10+ | `pbir`, scripts, SVG/measure tooling | n/a | python.org / Store |
| `jq` | hooks (`04-review/hooks/`) JSON checks | No | platform package manager |
| Power BI Desktop | the target tool | **Yes** | Microsoft Store / direct download |
| PowerShell 7+ | `03-bind/` scripts | **Yes** | pre-installed on Windows |
| TOM / ADOMD.NET (NuGet) | `03-bind/` live model | **Yes** | `winget install Microsoft.NuGet` (self-installs on first use) |
| Power BI Modeling MCP | model mutations (measures/columns/relationships), MCP-first | **Yes** (Microsoft) | npx `@microsoft/powerbi-modeling-mcp` or the VS Code extension — needs Node.js + Desktop open. [Section ↓](#power-bi-modeling-mcp-model-mutations) |
| Desktop Bridge CLI (`powerbi-desktop`) | reload + screenshot the open report (visual-verify loop, `03-bind/desktop-bridge.md`) | **Yes** (Microsoft, preview) | `npm i -g @microsoft/powerbi-desktop-bridge-cli` (auto by `setup.ps1`) |
| Report Authoring CLI (`powerbi-report-author`) | first-party PBIR authoring + `validate` (alternative to `pbir`) | **Yes** (Microsoft, preview) | `npm i -g @microsoft/powerbi-report-authoring-cli` (optional) |
| Node.js 18+ | runs the Modeling MCP (npx) + the Desktop Bridge / Report Authoring CLIs | n/a | `winget install OpenJS.NodeJS.LTS` |

> PBIR is a **preview** format — enable it in Desktop: *File → Options → Preview features → "Store
> reports using enhanced metadata format (PBIR)"*, then save/convert the project.
