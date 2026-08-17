#Requires -Version 5.1
<#
.SYNOPSIS
  Bootstrap external dependencies for the Power BI blueprint. See 00-setup.md.

.DESCRIPTION
  Default run (non-destructive): verifies Python, installs/updates the pbir CLI (>= 0.9.25) via pip,
  and reports whether jq + Power BI Desktop are present.
  Add -InstallMissing to also winget-install Python / jq / Power BI Desktop when they're absent.

.NOTES
  pbir-cli is a COMMUNITY tool (Kurt Buhler & Maxim Anatsko) under a Custom Non-Commercial License.
  Commercial use requires the authors' permission. It is NOT a Microsoft product. See 00-setup.md.

.EXAMPLE
  pwsh ./setup.ps1
.EXAMPLE
  pwsh ./setup.ps1 -InstallMissing
#>
[CmdletBinding()]
param([switch]$InstallMissing)

$MinPbir = [version]'0.9.25'
function Test-Cmd($n) { [bool](Get-Command $n -ErrorAction SilentlyContinue) }
function Say($m, $c = 'Gray') { Write-Host $m -ForegroundColor $c }
function Install-Winget($id) {
  if (-not (Test-Cmd winget)) { Say "       winget unavailable - install '$id' manually" Yellow; return }
  winget install -e --id $id --accept-package-agreements --accept-source-agreements
}

Say "`n== Power BI blueprint - dependency setup ==" Cyan
Say "pbir-cli is a COMMUNITY, NON-COMMERCIAL-licensed tool (not Microsoft). See 00-setup.md.`n" DarkYellow

# 1) Python (host for pbir + scripts)
if (Test-Cmd python) { Say "[ok]   $(python --version 2>&1)" Green }
else {
  Say "[miss] Python 3.10+ not found" Yellow
  if ($InstallMissing) { Install-Winget 'Python.Python.3.11' }
  else { Say "       -> winget install Python.Python.3.11   (or re-run with -InstallMissing)" Yellow }
}

# 2) pbir CLI (the core dependency)
if (Test-Cmd python) {
  Say "`n[*]    installing / updating pbir-cli ..." Gray
  python -m pip install -U pbir-cli
}
if (Test-Cmd pbir) {
  $out = (pbir --version) 2>&1
  if ($out -match '(\d+\.\d+\.\d+)') {
    $v = [version]$Matches[1]
    if ($v -ge $MinPbir) { Say "[ok]   pbir $v (>= $MinPbir)" Green }
    else { Say "[warn] pbir $v < $MinPbir  ->  python -m pip install -U pbir-cli" Yellow }
  }
  else { Say "[ok]   pbir installed ($out)" Green }
}
else {
  Say "[err]  'pbir' not on PATH after install. Add your Python 'Scripts' folder to PATH, reopen the shell." Red
}

# 3) jq (used by 04-review hooks)
if (Test-Cmd jq) { Say "[ok]   jq present" Green }
elseif ($InstallMissing) { Install-Winget 'jqlang.jq' }
else { Say "[miss] jq (04-review hooks)  ->  winget install jqlang.jq" Yellow }

# 4) Power BI Desktop (the target tool; Windows-only)
$pbi = (Test-Cmd PBIDesktop) -or [bool](Get-AppxPackage -Name '*PowerBIDesktop*' -ErrorAction SilentlyContinue)
if ($pbi) { Say "[ok]   Power BI Desktop detected" Green }
elseif ($InstallMissing) { Install-Winget 'Microsoft.PowerBI' }
else { Say "[miss] Power BI Desktop  ->  winget install Microsoft.PowerBI  (or Microsoft Store)" Yellow }

# 5) Node.js + Power BI first-party CLIs (Microsoft, npm)
if (Test-Cmd node) {
  Say "[ok]   Node $(node --version)" Green
  # Desktop Bridge CLI — reload + screenshot the open report (visual verify loop)
  Say "[*]    installing @microsoft/powerbi-desktop-bridge-cli@latest ..." Gray
  npm install -g '@microsoft/powerbi-desktop-bridge-cli@latest' 2>&1 | Out-Null
  if (Test-Cmd powerbi-desktop) { Say "[ok]   powerbi-desktop $(powerbi-desktop --version)" Green }
  else { Say "[warn] 'powerbi-desktop' not on PATH yet — reopen the shell" Yellow }
  Say "       Optional first-party extras (not auto-installed):" DarkGray
  Say "         npm i -g @microsoft/powerbi-report-authoring-cli   # 'powerbi-report-author validate' (MS's PBIR validator, alt to pbir)" DarkGray
  Say "         Modeling MCP runs via npx @microsoft/powerbi-modeling-mcp (wired by .mcp.json, step 6 below)" DarkGray
}
elseif ($InstallMissing) { Install-Winget 'OpenJS.NodeJS.LTS' }
else { Say "[miss] Node.js (Desktop Bridge CLI + Modeling MCP)  ->  winget install OpenJS.NodeJS.LTS" Yellow }

# 6) .mcp.json — ensure the Power BI Modeling MCP is wired for Claude Code (self-heal).
#    Content is machine-invariant (npx @latest, no absolute paths), so a static write is safe.
#    Lives at the WORKSPACE ROOT (one level above this power-bi/ folder).
$McpPath = Join-Path (Split-Path $PSScriptRoot -Parent) '.mcp.json'
$McpJson = @'
{
  "mcpServers": {
    "powerbi-modeling-mcp": {
      "type": "stdio",
      "command": "npx",
      "args": [
        "-y",
        "@microsoft/powerbi-modeling-mcp@latest",
        "--start",
        "--skipconfirmation"
      ],
      "env": {}
    }
  }
}
'@
$McpOk = $false
if (Test-Path $McpPath) {
  try { Get-Content $McpPath -Raw | ConvertFrom-Json | Out-Null; $McpOk = $true } catch { $McpOk = $false }
}
if ($McpOk) { Say "`n[ok]   .mcp.json present (Power BI Modeling MCP wired)" Green }
else {
  Say "`n[*]    writing .mcp.json (Power BI Modeling MCP) ..." Gray
  # WriteAllText emits UTF-8 WITHOUT a BOM on both PS 5.1 and 7+ (Set-Content -Encoding UTF8 adds a BOM on 5.1).
  [System.IO.File]::WriteAllText($McpPath, $McpJson)
  Say "[ok]   wrote $McpPath  -> restart Claude Code to load the MCP" Green
}

Say "`nNext:" Cyan
Say "  - Enable PBIR in Desktop: File > Options > Preview features > 'Store reports using enhanced metadata format (PBIR)'." Gray
Say "  - Power BI Modeling MCP (model edits, MCP-first): VS Code extension (aka.ms/powerbi-modeling-mcp-vscode)" Gray
Say "    or stdio config -> npx -y @microsoft/powerbi-modeling-mcp@latest --start  (needs Node + Desktop open)." Gray
Say "  - 03-bind/ (live model) self-installs TOM/NuGet on first use." Gray
Say "  - Full details, license, and the hand-edit fallback: 00-setup.md.`n" Gray
