# Post-rename verification

After any cascade rename, run these checks before declaring done.

```bash
PROJ="<project>"
OLD="\[Old Name\]"   # or 'Old Table'  or  [Old Column]

# 1. Zero matches of the old name anywhere
grep -rn "$OLD" "$PROJ.Report/" "$PROJ.SemanticModel/"

# 2. PBIR validates clean
pbir validate "$PROJ.Report"

# 3. TMDL validates clean
bash ../04-review/hooks/validate-tmdl.sh "$PROJ.SemanticModel"

# 4. Both DAXQueries directories checked
grep -rn "$OLD" "$PROJ.SemanticModel/DAXQueries/" "$PROJ.Report/DAXQueries/"
```

If any step returns hits, the rename is incomplete — open each match and fix.

Then reopen the project in Power BI Desktop to confirm no broken visual badges.
