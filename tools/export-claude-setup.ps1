#Requires -Version 5.1
<#
.SYNOPSIS
  Snapshot the portable Claude Code user setup into one zip.

.DESCRIPTION
  Read-only — safe to run at any time; re-run whenever settings/memory changed.
  Collects exactly the four portable pieces from ~/.claude:
    1. settings.json                      (model, permissions, plugins + marketplaces)
    2. commands\sc\                       (SuperClaude /sc:* command set)
    3. agents\                            (custom agent definitions)
    4. projects\<workspace-key>\memory\   (Claude's memory for THIS workspace)
  plus a manifest.json so import-claude-setup.ps1 can re-key the memory folder
  when the new machine clones the workspace to a different path.

  Deliberately NOT exported: ~/.claude.json (OAuth/account/machine state — just
  `claude login` on the new machine), caches, sessions, history.

.EXAMPLE
  pwsh tools/export-claude-setup.ps1
  pwsh tools/export-claude-setup.ps1 -OutFile D:\backup\claude-setup.zip
#>
[CmdletBinding()]
param(
  [string]$OutFile = (Join-Path (Get-Location) ("claude-setup-{0}.zip" -f (Get-Date -Format yyyy-MM-dd)))
)

$claude = Join-Path $env:USERPROFILE '.claude'
if (-not (Test-Path $claude)) { throw "~/.claude not found at $claude — is Claude Code installed?" }

# workspace root = parent of this script's tools/ folder; derive its memory key
$workspace = Split-Path $PSScriptRoot -Parent
$key = ($workspace -replace '[:\\/]', '-')
$key = $key.Substring(0,1).ToLower() + $key.Substring(1)   # E:\Workspace-Blueprint -> e--Workspace-Blueprint

$stage = Join-Path $env:TEMP ("claude-export-" + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $stage | Out-Null
$copied = @()

function Copy-Piece($src, $dst, $label) {
  if (Test-Path $src) {
    New-Item -ItemType Directory -Path (Split-Path $dst -Parent) -Force | Out-Null
    Copy-Item $src $dst -Recurse -Force
    $script:copied += $label
    Write-Host "[ok]   $label" -ForegroundColor Green
  } else {
    Write-Host "[skip] $label (not found: $src)" -ForegroundColor Yellow
  }
}

Copy-Piece (Join-Path $claude 'settings.json')                       (Join-Path $stage 'settings.json')                       'settings.json'
Copy-Piece (Join-Path $claude 'commands\sc')                         (Join-Path $stage 'commands\sc')                         'commands\sc  (SuperClaude)'
Copy-Piece (Join-Path $claude 'agents')                              (Join-Path $stage 'agents')                              'agents'
Copy-Piece (Join-Path $claude "projects\$key\memory")                (Join-Path $stage "projects\$key\memory")                "projects\$key\memory  (workspace memory)"

@{
  exported      = (Get-Date -Format s)
  sourceMachine = $env:COMPUTERNAME
  workspacePath = $workspace
  workspaceKey  = $key
  pieces        = $copied
} | ConvertTo-Json | Set-Content (Join-Path $stage 'manifest.json') -Encoding UTF8

if (Test-Path $OutFile) { Remove-Item $OutFile -Force }
Compress-Archive -Path (Join-Path $stage '*') -DestinationPath $OutFile
Remove-Item $stage -Recurse -Force

Write-Host "`nExported $($copied.Count) piece(s) -> $OutFile" -ForegroundColor Cyan
Write-Host "On the new machine: install Claude Code, 'claude login', clone the workspace, then:" -ForegroundColor Gray
Write-Host "  pwsh tools/import-claude-setup.ps1 -Zip <path-to-this-zip>" -ForegroundColor Gray
