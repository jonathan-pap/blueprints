# PBIX file encoding

Mixed encodings inside a PBIX. Reading or writing with the wrong one causes parse failures.

| File | Encoding |
|---|---|
| `Version`, `Settings`, `Metadata` | UTF-16LE |
| `Connections` | UTF-8 |
| `Report/definition/` contents | UTF-8 |
| `Report/Layout` (legacy) | UTF-16LE |
| `[Content_Types].xml` | UTF-8 **with BOM** |
| `SecurityBindings`, `DataModel` | Binary |

PBIP-side files (`<name>.Report/`, `<name>.SemanticModel/`) are all **UTF-8 without BOM**. A BOM here breaks parsers — see `validate-utf8-no-bom.md`.
