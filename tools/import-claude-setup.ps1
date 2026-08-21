#Requires -Version 5.1
<#
.SYNOPSIS
  Restore a claude-setup zip (from export-claude-setup.ps1) into this machine's ~/.claude.

.DESCRIPTION
  Run AFTER installing Claude Code + `claude login`, from inside the cloned workspace
  (the script re-keys the memory folder to THIS machine's workspace path automatically).
  Existing settings.json is backed up to settings.json.bak before being replaced.

.EXAMPLE
  pwsh tools/import-claude-setup.ps1 -Zip C:\Users\me\Downloads\claude-setup-2026-08-21.zip
#>
[CmdletBinding()]
param(
  [Parameter(Mandatory)][string]$Zip
)

if (-not (Test-Path $Zip)) { throw "Zip not found: $Zip" }
$claude = Join-Path $env:USERPROFILE '.claude'
New-Item -ItemType Directory -Path $claude -Force | Out-Null

$stage = Join-Path $env:TEMP ("claude-import-" + [guid]::NewGuid().ToString('N'))
Expand-Archive -Path $Zip -DestinationPath $stage
$manifest = Get-Content (Join-Path $stage 'manifest.json') -Raw | ConvertFrom-Json

# this machine's workspace key (script lives in <workspace>\tools\)
$workspace = Split-Path $PSScriptRoot -Parent
$newKey = ($workspace -replace '[:\\/]', '-')
$newKey = $newKey.Substring(0,1).ToLower() + $newKey.Substring(1)

# 1) settings.json (backup existing first)
$src = Join-Path $stage 'settings.json'
if (Test-Path $src) {
  $dst = Join-Path $claude 'settings.json'
  if (Test-Path $dst) { Copy-Item $dst "$dst.bak" -Force; Write-Host "[ok]   backed up existing settings.json -> settings.json.bak" -ForegroundColor Yellow }
  Copy-Item $src $dst -Force
  Write-Host "[ok]   settings.json (plugins/marketplaces auto-install on next launch)" -ForegroundColor Green
}

# 2+3) commands\sc + agents (merge-copy)
foreach ($piece in @('commands\sc', 'agents')) {
  $src = Join-Path $stage $piece
  if (Test-Path $src) {
    $dst = Join-Path $claude $piece
    New-Item -ItemType Directory -Path (Split-Path $dst -Parent) -Force | Out-Null
    Copy-Item $src $dst -Recurse -Force
    Write-Host "[ok]   $piece" -ForegroundColor Green
  }
}

# 4) workspace memory — re-key from the source machine's path to this one's
$srcMem = Join-Path $stage ("projects\{0}\memory" -f $manifest.workspaceKey)
if (Test-Path $srcMem) {
  $dstMem = Join-Path $claude ("projects\{0}\memory" -f $newKey)
  New-Item -ItemType Directory -Path (Split-Path $dstMem -Parent) -Force | Out-Null
  Copy-Item $srcMem $dstMem -Recurse -Force
  if ($newKey -ne $manifest.workspaceKey) {
    Write-Host "[ok]   memory re-keyed: $($manifest.workspaceKey) -> $newKey" -ForegroundColor Green
  } else {
    Write-Host "[ok]   memory ($newKey)" -ForegroundColor Green
  }
}

Remove-Item $stage -Recurse -Force
Write-Host "`nDone. Launch Claude Code inside $workspace — approve the .mcp.json trust prompt on first run." -ForegroundColor Cyan
