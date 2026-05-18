# Annotation — CRUD

Key/value metadata attached to almost any TOM object. Useful for marking provenance, tool versions, custom flags.

## Add

```powershell
$ann = New-Object Microsoft.AnalysisServices.Tabular.Annotation
$ann.Name  = "GeneratedBy"
$ann.Value = "claude-workspace-blueprint"
$model.Tables["Sales"].Annotations.Add($ann)
$model.SaveChanges()
```

## Read

```powershell
$model.Tables["Sales"].Annotations | Select-Object Name, Value
$model.Tables["Sales"].Annotations["GeneratedBy"].Value
```

## Update

```powershell
$model.Tables["Sales"].Annotations["GeneratedBy"].Value = "v2"
$model.SaveChanges()
```

## Delete

```powershell
$t = $model.Tables["Sales"]
$t.Annotations.Remove($t.Annotations["GeneratedBy"])
$model.SaveChanges()
```

## Which objects support annotations

Almost all: `Model`, `Database`, `Table`, `Column`, `Measure`, `Hierarchy`, `Level`, `Partition`, `Role`, `Perspective`, `Culture`, `Relationship`, `Expression`, `DataSource`, `QueryGroup`, `Function`.

## See also

`../annotations.md` — broader patterns including `ExtendedProperty` (structured JSON values) and `PBI_*` annotations that Power BI Desktop manages automatically.
