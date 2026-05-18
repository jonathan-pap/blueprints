# Validate UTF-8 without BOM

PBIP files must be UTF-8 **without** a byte-order mark. A BOM at the start of a file breaks `jq`, `tmdl-validate`, and other parsers.

## Detect

```bash
# List any files in the project that start with a BOM (EF BB BF)
find "<project>.Report" "<project>.SemanticModel" -type f \
  \( -name "*.json" -o -name "*.tmdl" -o -name "*.pbir" \) \
  -exec sh -c 'head -c3 "$1" | grep -q "^$(printf "\xEF\xBB\xBF")" && echo "$1"' _ {} \;
```

## Fix

```bash
# Strip BOM in place
sed -i '1s/^\xEF\xBB\xBF//' path/to/file.json
```

## Why

Power BI Desktop writes files without BOM. External editors (VS Code with the wrong setting, Notepad, some Windows tools) silently add one when saving. The hook in `../../../04-review/hooks/validate-pbir.sh` catches BOM-prefixed files via `jq` parse failure.

## Prevent

In VS Code: settings → `"files.encoding": "utf8"` (NOT `"utf8bom"`).
In Git: `* text=auto` in `.gitattributes` plus `core.autocrlf` configured.
