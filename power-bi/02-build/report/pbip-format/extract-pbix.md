# Extract a PBIX

A `.pbix` is a ZIP archive (OPC). Extract to inspect or to hand-assemble a PBIP.

## Python (with zip-slip protection)

```python
import zipfile
from pathlib import Path

pbix = Path("MyReport.pbix")
out  = Path("MyReport_extracted")
resolved = out.resolve()

with zipfile.ZipFile(pbix, "r") as z:
    for m in z.infolist():
        if not (out / m.filename).resolve().is_relative_to(resolved):
            raise ValueError(f"zip slip: {m.filename}")
    z.extractall(out)

is_thick  = (out / "DataModel").exists()
is_legacy = (out / "Report" / "Layout").exists()
is_modern = (out / "Report" / "definition" / "report.json").exists()
```

## Bash

```bash
unzip MyReport.pbix -d MyReport_extracted/
```

## What you'll find

- `DataModel` (binary) → **thick** PBIX. Cannot be programmatically read.
- `Connections` (JSON) → **thin** PBIX.
- `Report/definition/` → modern PBIR layout.
- `Report/Layout` → legacy monolithic JSON.

Next step → `pbix-encoding-table.md` for per-file encoding rules.
