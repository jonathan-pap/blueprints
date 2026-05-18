# Quickstart — connect to Power BI Desktop

Get a TOM session in five steps. For canned end-to-end, run `scripts/connect-and-enumerate.ps1`.

## Prereqs

- PBI Desktop open with a thick model loaded.
- PowerShell (Windows native; macOS via Parallels — see `parallels-macos.md`).
- NuGet CLI: `winget install Microsoft.NuGet`.

## Install TOM + ADOMD (once per machine)

```powershell
$pkgDir = "$env:TEMP\tom_nuget"
foreach ($pkg in @("Microsoft.AnalysisServices.retail.amd64","Microsoft.AnalysisServices.AdomdClient.retail.amd64")) {
  if (-not (Test-Path "$pkgDir\$pkg")) {
    nuget install $pkg -OutputDirectory $pkgDir -ExcludeVersion
  }
}
```

## End-to-end snippet

```powershell
# 1. Find ports
$pids  = (Get-Process msmdsrv -ErrorAction SilentlyContinue).Id
$ports = netstat -ano | Select-String "LISTENING" |
    Where-Object { $pids -contains ($_ -split "\s+")[-1] } |
    ForEach-Object { ($_ -split "\s+")[2] -replace ".*:" }

# 2. Load TOM
$basePath = "$env:TEMP\tom_nuget\Microsoft.AnalysisServices.retail.amd64\lib\net45"
Add-Type -Path "$basePath\Microsoft.AnalysisServices.Core.dll"
Add-Type -Path "$basePath\Microsoft.AnalysisServices.Tabular.dll"

# 3. Connect
$server = New-Object Microsoft.AnalysisServices.Tabular.Server
$server.Connect("Data Source=localhost:$($ports[0])")
$model  = $server.Databases[0].Model

# 4. Use $model (enumerate, query, modify) …

# 5. Always disconnect
$server.Disconnect()
```

## Multi-instance gotcha

Multiple PBI Desktop files = multiple ports. Iterate, read `$server.Databases[0].Name`, ask the user which one if more than one shows up.

## Constraints

- Localhost only. Direct Lake / Fabric-hosted models are unreachable through this path — use Power BI MCP (`../via-mcp/`) for those.
- `-ExecutionPolicy Bypass` is required when invoking PowerShell scripts from Bash.
- When piping commands via Bash, single-quote `-Command` args (Bash eats `$` otherwise).

## Next

- Read model → `../via-mcp/list-tables.md` (preferred) or DMVs via `query-dax.md`.
- Query → `query-dax.md`.
- Mutate → `modify-tom.md`.
