# Convert PBIX → PBIP

The canonical path is Power BI Desktop's File → Save As. There is no fully reliable CLI converter.

## Procedure

1. Open the `.pbix` in Power BI Desktop.
2. File → Save As → choose **Power BI Project (`.pbip`)**.
3. Pick the output folder. Desktop creates `<name>.pbip`, `<name>.Report/`, and (for thick) `<name>.SemanticModel/`.
4. Close Desktop.
5. Validate the output:

```bash
pbir validate "<name>.Report"
```

## Reverse direction (PBIP → PBIX)

Same dialog: open the `.pbip`, Save As, choose `.pbix`. Useful for sharing with consumers who don't have PBIP-aware tooling.

## After

Commit `<name>.Report/` and `<name>.SemanticModel/` to Git. `.pbix` should be gitignored.
