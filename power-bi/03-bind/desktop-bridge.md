# Power BI Desktop Bridge — reload + screenshot the open report (visual verify loop)

> **Status: preview, opt-in. Verified working end-to-end 2026-07-01** with the official CLI
> `@microsoft/powerbi-desktop-bridge-cli` v0.1.1 — launched Desktop, reloaded on-disk edits, and captured
> pages (incl. confirming an SVG-in-cell fix visually). Gated by **`desktop_bridge`** in
> [`via-powershell/hooks/config.yaml`](via-powershell/hooks/config.yaml). Preview — the API may change.
> Docs: [Desktop Bridge overview](https://learn.microsoft.com/en-us/power-bi/developer/agentic/power-bi-desktop-bridge-overview).

## What it is

A local server **hosted inside the running Power BI Desktop process** (named pipe
`pbi-desktop-bridge-<pid>`, JSON-RPC 2.0, local-only, one op at a time). It exposes exactly **three
methods** — `application.state.get/v1`, `file.reload/v1`, `report.snapshot.capture/v1` (+ `bridge.manifest`
for discovery). **Drive it with the first-party CLI**, not raw pipes. This unlocks a real-time loop:

> **edit PBIR/TMDL on disk → `powerbi-desktop reload` → `powerbi-desktop screenshot` → read the PNG →
> iterate**, with Desktop **staying open** the whole time.

It is **not** the Modeling MCP: MCP = model + data edits; Bridge = report **reload + screenshot + state**.
It doesn't replace `pbir validate` either — the Bridge shows the *rendered* result; `pbir` checks *structure*.

## Setup

```bash
npm install -g @microsoft/powerbi-desktop-bridge-cli    # (setup.ps1 auto-installs when Node is present)
powerbi-desktop --version
```

Enable the Desktop preview feature (on by default): *File → Options → Preview features → "Enable external
tool access to Power BI Desktop through secure local APIs"*.

**Store-installed Desktop:** `powerbi-desktop open` may fail with `DESKTOP_EXE_NOT_FOUND` because the Store
build lives under a protected `WindowsApps` path. Either install the **standalone `.exe`** build (lands at
`C:\Program Files\Microsoft Power BI Desktop\bin\PBIDesktop.exe`, which the CLI finds), or set
`PBI_DESKTOP_PATH` to the real exe. Other verbs (`status`/`reload`/`screenshot`) don't need it — they attach
to an already-running Desktop.

## The command loop

```bash
powerbi-desktop open "<path.pbip>"                                   # launch Desktop with a report
powerbi-desktop status                                               # instances[]: pid, bridgeStatus, currentFilePath, reportDir, pages[]
powerbi-desktop manifest --pid <pid>                                 # methods this Desktop build supports
powerbi-desktop reload --pid <pid> --wait-seconds 120                # re-read PBIP/PBIR (+ TMDL) from disk in place
powerbi-desktop screenshot <pageId> --pid <pid> --wait-seconds 120 --output page.png
powerbi-desktop screenshot-all --pid <pid> --wait-seconds 120 --output-dir shots
```

- **`status` gives you everything**: pick the PID where `bridgeStatus: connected` and `currentFilePath`
  matches your target; its `pages[]` lists every `id` + `displayName` (no need to read `pages.json`).
- **`screenshot <pageId>`** takes the **internal PBIR page id** (the hex folder under
  `definition/pages/`, e.g. `15508c150e844a98`), **not** the display name. Defaults to **`--scale 2`**
  (1–3). The capture includes the right-hand **filter pane** (`outspacePane`) — collapse it report-wide
  with `objects.outspacePane.expanded=false` for cleaner shots (see `../02-build/report/filters/configure-filter-pane.md`).
- **`open <path>` is the only verb that takes a path**; the rest target a running instance by `--pid`.
  `screenshot-all` loops capture over every page (CLI convenience; the bridge itself is per-`pageId`).

## The 30s timeout — use `--wait-seconds`

The bridge has a **30-second default render budget**; heavy pages return `-32504 exceeded timeout of 30s`.
This is **render time, not output size** (`--scale 1` doesn't help). Two triggers seen live:

1. **Expensive pages** — SVG-in-cell tableExes and 12–22-visual pages blow past 30s.
2. **A model that isn't fully loaded/refreshed** — right after `open`, or when calc tables were edited on
   disk, *every* page (even light cards) can hang until the model is refreshed. **New calc tables need a
   refresh** (the bridge can't refresh — that's a model op via the MCP or Desktop UI).

Fix: raise the budget, e.g. `--wait-seconds 120`. `screenshot 15508c150e844a98 --wait-seconds 120` captured
a heavy SVG page that failed at the raw 30s. To verify a *measure's value* when capture won't cooperate,
evaluate it via the MCP (`dax_query_operations`) instead.

## Rules & gotchas

- **Serial per PID.** Never run `reload`/`screenshot` in parallel against the same PID → `Cancelled`.
  `status`/`manifest` are safe concurrently.
- **Save-first / clobber guard.** `reload` makes disk win — if Desktop has real unsaved edits
  (`status → hasUnsavedChanges: true`), reloading discards them ([[pbi-desktop-clobbers-tmdl]]). (Desktop
  auto-dirties the model on open; that's harmless to reload over.)
- **Theme JSON reload cache.** Editing an existing theme file may not take on `reload` — theme files are
  cache-keyed by filename. Rename the theme file (+ update `report.json`) or reopen Desktop.
- **`reload` is PBIP/PBIR-only** — a `.pbix`-only PID returns `REPORT_DIR_REQUIRED`.

## Error codes (CLI)

| Code | Meaning / fix |
|---|---|
| `DESKTOP_EXE_NOT_FOUND` | `open` can't find `PBIDesktop.exe` (Store build) — set `PBI_DESKTOP_PATH` or install the `.exe` build |
| `not_connected` / `NO_BRIDGE` | Desktop closed, or preview toggle off — `open` a report / enable the toggle / `status --wait-seconds 30` |
| `AMBIGUOUS_DESKTOP_INSTANCE` | multiple bridges — pick a PID from `status`, pass `--pid` |
| `METHOD_NOT_AVAILABLE` | Desktop build too old for a method — update Desktop |
| `REPORT_DIR_REQUIRED` | selected PID has only a `.pbix` open — pick a PBIP PID or `open` the target |
| `Timeout` (`-32504`) | render exceeded budget — rerun with `--wait-seconds 120`; if persistent the model is genuinely slow / needs refresh |
| `Cancelled` | a concurrent reload/screenshot ran on the same PID — serialize per PID |

## No-CLI fallback (raw named pipe)

If the CLI isn't available, drive the pipe directly (JSON-RPC 2.0, Content-Length framing):

```powershell
function Write-Frame($s,$p){ $j=$p|ConvertTo-Json -Depth 12 -Compress; $b=[Text.Encoding]::UTF8.GetBytes($j)
  $h=[Text.Encoding]::ASCII.GetBytes("Content-Length: $($b.Length)`r`n`r`n"); $s.Write($h,0,$h.Length); $s.Write($b,0,$b.Length); $s.Flush() }
function Read-Frame($s){ $hd=''; while(-not $hd.EndsWith("`r`n`r`n")){ $x=$s.ReadByte(); if($x -eq -1){throw 'closed'}; $hd+=[char]$x }
  $len=[int]([regex]::Match($hd,'Content-Length:\s*(\d+)').Groups[1].Value); $buf=New-Object byte[] $len; $o=0
  while($o -lt $len){ $r=$s.Read($buf,$o,$len-$o); if($r -eq 0){throw 'short'}; $o+=$r }; [Text.Encoding]::UTF8.GetString($buf) }
function Invoke-Bridge($method,$args=@{}){
  $p=(Get-Process PBIDesktop -EA SilentlyContinue|?{Test-Path "\\.\pipe\pbi-desktop-bridge-$($_.Id)"}|Select -First 1)
  if(-not $p){throw 'No Desktop bridge pipe — open Desktop with the preview toggle on.'}
  $pipe=New-Object IO.Pipes.NamedPipeClientStream('.',"pbi-desktop-bridge-$($p.Id)",[IO.Pipes.PipeDirection]::InOut); $pipe.Connect(5000)
  Write-Frame $pipe @{ jsonrpc='2.0'; id=1; method=$method; params=@{ args=$args } }
  try { (Read-Frame $pipe | ConvertFrom-Json) } finally { $pipe.Dispose() } }

Invoke-Bridge 'application.state.get/v1'
Invoke-Bridge 'file.reload/v1' @{ reloadModelDefinition=$true }
$r = Invoke-Bridge 'report.snapshot.capture/v1' @{ pageId='<hex-page-id>'; scale=2.0 }
[IO.File]::WriteAllBytes("$env:TEMP\page.png", [Convert]::FromBase64String($r.result.payload))
```

Note the raw method has **only the 30s budget** (no `--wait-seconds`) — the CLI's retry budget is why it
beats the raw pipe on heavy pages.

## Related first-party CLIs

- **`@microsoft/powerbi-report-authoring-cli`** (`powerbi-report-author validate`) — MS's first-party PBIR
  authoring + validator; the same skill family drives this exact bridge loop (`microsoft/skills-for-fabric`).
- **`@microsoft/powerbi-modeling-mcp`** — model edits (see [`../00-setup.md`](../00-setup.md#power-bi-modeling-mcp-model-mutations)).
