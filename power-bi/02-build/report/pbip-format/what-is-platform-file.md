# What is a `.platform` file

Tiny JSON next to most PBIP folders. Carries the item's GUID, display name, and platform metadata.

## Example

`<project>.Report/.platform`:

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/fabric/platform/2.0.0/schema.json",
  "metadata": {
    "type": "Report",
    "displayName": "Sales Overview"
  },
  "config": {
    "version": "2.0",
    "logicalId": "<guid>"
  }
}
```

## Rules

- **Never delete** — Power BI re-creates it but Fabric loses the deployment link.
- **Never edit the `logicalId` GUID** — it ties the local item to a published item in Fabric.
- The `displayName` is safe to edit (it's the Fabric workspace label).
- `.platform` files exist for each item type: `.Report`, `.SemanticModel`, etc.

## When you see one outside expected locations

A stray `.platform` usually means a copy/paste error or an interrupted save. Diff against a known-good project before deleting.
