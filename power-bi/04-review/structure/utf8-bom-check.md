# Check for UTF-8 BOM

Power BI Desktop writes UTF-8 without BOM. External editors (Notepad, mis-configured VS Code) silently add a BOM, which breaks `jq`, `tmdl-validate`, and Power BI itself.

## Detect

```bash
find "<project>.Report" "<project>.SemanticModel" -type f \
  \( -name "*.json" -o -name "*.tmdl" -o -name "*.pbir" \) \
  -exec sh -c 'head -c3 "$1" | grep -q "^$(printf "\xEF\xBB\xBF")" && echo "$1"' _ {} \;
```

Lists every file that starts with a BOM.

## Strip

```bash
# Single file
sed -i '1s/^\xEF\xBB\xBF//' path/to/file.json

# All BOM-prefixed files in a project
find "<project>" -type f \( -name "*.json" -o -name "*.tmdl" -o -name "*.pbir" \) \
  -exec sh -c 'head -c3 "$1" | grep -q "^$(printf "\xEF\xBB\xBF")" && sed -i "1s/^\xEF\xBB\xBF//" "$1" && echo "Stripped: $1"' _ {} \;
```

## Prevent

- **VS Code**: settings → `"files.encoding": "utf8"` (NOT `"utf8bom"`).
- **Notepad++**: Encoding → Convert to UTF-8 (no BOM).
- **PowerShell `Out-File`**: use `-Encoding utf8NoBOM` (PS 7+) or pipe through `[System.IO.File]::WriteAllText()`.
- **Git**: `.gitattributes` with `* text=auto eol=lf` (note: doesn't fix BOM, but normalises line endings).

## Wired

`hooks/validate-pbir.sh` already catches BOM via `jq empty` parse failure on every PostToolUse. Strip pre-commit or fix on detection.
