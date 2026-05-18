# Consumers `downstream-reports.md` does NOT find

A semantic model can be consumed by many things besides Power BI reports. The script only catches reports.

## Not detected

- **Analyze in Excel workbooks** (.xlsx live connections to the model)
- **Composite models** — other semantic models chaining via DirectQuery
- **Explorations** — ad-hoc visual explorations in the Power BI service
- **Fabric notebooks** — connecting via Spark, sempy, or semantic-link
- **Fabric data agents**
- **Paginated reports** (.rdl)
- **Dataflows** referencing the model
- **Third-party tools** connecting via XMLA (Tableau, Excel via XMLA, custom apps)

## How to find these

For full dependency mapping including all item types, use the official Fabric lineage API:

```bash
fab api "admin/groups/{workspace-id}/lineage"
```

Requires **tenant admin role**. Returns edges between datasets, dataflows, reports, dashboards, notebooks, and downstream artifacts.

For a UI view: Power BI Service → workspace → Lineage view (same data, visual presentation).

## When this matters

Impact analysis before deleting / renaming a model:

1. Run `downstream-reports.md` for the reports.
2. Run `fab api "admin/groups/{ws}/lineage"` if you have admin to catch everything else.
3. If no admin access, manually check with the data team about Excel, notebooks, and third-party connections.

A "no downstream reports" result from `downstream-reports.md` does NOT mean the model is unused.
