# Convert legacy report.json → PBIR

Older PBIX files store the report as a single `Report/Layout` monolithic JSON (UTF-16LE). PBIR uses a folder of small JSON files. Convert before editing.

## Detect legacy

After extracting a PBIX (see `../pbip-format/extract-pbix.md`), check:

```bash
ls Report/Layout 2>/dev/null   # legacy if present
ls Report/definition/          # modern PBIR
```

## Convert

Open the PBIX in Power BI Desktop → File → Save As → choose **Power BI Project**. Desktop converts the monolith into the PBIR folder structure.

There is no fully reliable CLI converter — Desktop is the canonical path. If Desktop is unavailable, run the helper script:

```bash
python ../scripts/convert_legacy_to_pbir.py path/to/Report/Layout path/to/output.Report
```

Handles the common cases; complex reports may need manual fixup afterwards.

## After

Validate the converted output:

```bash
pbir validate "<project>.Report"
```

Open in Desktop once to verify nothing rendered incorrectly. Then commit.
