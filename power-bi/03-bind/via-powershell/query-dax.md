# Query DAX (ADOMD.NET)

Run DAX after `quickstart.md` has connected. Prefer `../via-mcp/query-dax.md` when MCP is available.

## Open ADOMD connection

```powershell
Add-Type -Path "$env:TEMP\tom_nuget\Microsoft.AnalysisServices.AdomdClient.retail.amd64\lib\net45\Microsoft.AnalysisServices.AdomdClient.dll"
$conn = New-Object Microsoft.AnalysisServices.AdomdClient.AdomdConnection
$conn.ConnectionString = "Data Source=localhost:<PORT>"
$conn.Open()
```

## Read results correctly

ADOMD returns fully-qualified column names (`'Sales'[Amount]`). Short-name access returns blank silently. Iterate by index:

```powershell
$cmd = $conn.CreateCommand()
$cmd.CommandText = "EVALUATE SUMMARIZECOLUMNS('Date'[Year], ""@Total"", SUM('Sales'[Amount]))"
$reader = $cmd.ExecuteReader()
while ($reader.Read()) {
    for ($i = 0; $i -lt $reader.FieldCount; $i++) {
        Write-Output "$($reader.GetName($i)): $($reader.GetValue($i))"
    }
}
$reader.Close()
$conn.Close()
```

## DAX rules (must follow)

- Fully qualify columns: `'Sales'[Amount]`. Never `[Amount]`.
- Always single-quote table names, even simple ones: `'Sales'`.
- Measures are unqualified: `[Total Revenue]`.
- Double-quote strings in DAX; escape inside PowerShell here-strings as `""`.

## DMV (model metadata) queries

```powershell
$cmd.CommandText = "SELECT * FROM `$SYSTEM.TMSCHEMA_TABLES"
$cmd.CommandText = "SELECT * FROM `$SYSTEM.TMSCHEMA_MEASURES"
$cmd.CommandText = "SELECT * FROM `$SYSTEM.TMSCHEMA_COLUMNS"
```

Backtick the `$` to escape PowerShell variable expansion.

## See also

- `dax-pitfalls.md` — common bugs
- `dax-expressions.md` — DAX shapes
- `evaluateandlog-debugging.md` — per-step DAX trace
