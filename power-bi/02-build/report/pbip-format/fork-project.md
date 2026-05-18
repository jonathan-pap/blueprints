# Fork a project

Duplicate a PBIP project as a new project. Used for variant reports, A/B testing, branch-off work.

## Procedure

```bash
SRC="projects/sales-overview"
DST="projects/sales-overview-q2"
NEW_NAME="Sales-Overview-Q2"

# 1. Copy
cp -r "$SRC" "$DST"

# 2. Rename the inner folders + .pbip file
cd "$DST"
mv "Sales-Overview.Report"        "$NEW_NAME.Report"
mv "Sales-Overview.SemanticModel" "$NEW_NAME.SemanticModel"
mv "Sales-Overview.pbip"          "$NEW_NAME.pbip"

# 3. Update internal references
sed -i "s/Sales-Overview/$NEW_NAME/g" "$NEW_NAME.pbip"
sed -i "s/Sales-Overview/$NEW_NAME/g" "$NEW_NAME.Report/definition.pbir"

# 4. Regenerate logical IDs in .platform files so Fabric treats them as new items
# Edit each .platform file's config.logicalId to a new GUID

# 5. Validate
pbir validate "$NEW_NAME.Report"
```

## Critical

The `.platform` files in `.Report/` and `.SemanticModel/` carry GUIDs that tie them to specific Fabric items. **Generate new GUIDs** when forking — otherwise both projects appear to be the same Fabric item.

## After

`post-rename-checklist.md` on the new project. Open in Desktop to confirm everything loads.
