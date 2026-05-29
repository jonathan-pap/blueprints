#!/usr/bin/env bash
# audit-layout-consistency.sh — flag layout drift against a project's design-system.yaml.
#
# Checks every visual.json in a .Report against the project's design tokens:
#   - sub-pixel positions/sizes (x/y/width/height not whole numbers)   <- the worst symptom
#   - off-grid positions/sizes (not multiples of grid.snap_to)
#   - slicer type drift (a slicer-family visual whose type != defaults.slicer.type)
#   - slicer size drift (configured slicer type whose size != defaults.slicer.size)
# Visuals named in the yaml `overrides:` block are exempt.
#
# Usage:
#   bash audit-layout-consistency.sh "<project>.Report"      # manual audit: prints report, exit 0
#   bash audit-layout-consistency.sh --hook "<project>.Report"  # opt-in: findings -> stderr, exit 2
#
# design-system.yaml is OPTIONAL — if absent, the audit skips silently (exit 0).
# Dependency-light: needs python (3.x) on PATH; no pyyaml required. Skips silently if no python.

set -u

HOOK_MODE=0
if [ "${1:-}" = "--hook" ]; then HOOK_MODE=1; shift; fi
REPORT="${1:-}"

if [ -z "$REPORT" ]; then
  echo "usage: audit-layout-consistency.sh [--hook] <project>.Report" >&2
  exit 0
fi

# pick a python that actually runs (skip Windows Store alias stubs, which exist on PATH but error)
PY=""
for c in python python3 py; do
  if command -v "$c" >/dev/null 2>&1 && "$c" -c "import sys" >/dev/null 2>&1; then PY="$c"; break; fi
done
[ -z "$PY" ] && exit 0   # no usable python -> skip silently

"$PY" - "$REPORT" "$HOOK_MODE" <<'PYEOF'
import json, os, re, sys

report = sys.argv[1]
hook_mode = sys.argv[2] == "1"

report = report.rstrip("/\\")
proj_dir = os.path.dirname(report) or "."
yaml_path = os.path.join(proj_dir, "design-system.yaml")
if not os.path.isfile(yaml_path):
    sys.exit(0)  # tokens optional -> skip

text = open(yaml_path, encoding="utf-8").read()

# --- minimal token extraction (no pyyaml) ---------------------------------
def find_int(pattern, default=None):
    m = re.search(pattern, text)
    return int(m.group(1)) if m else default

snap = find_int(r"snap_to:\s*(\d+)", 16)
# defaults.slicer block
slicer_type = "slicer"
m = re.search(r"slicer:\s*\n((?:\s+.*\n)+)", text)
slicer_w = slicer_h = None
if m:
    block = m.group(1)
    mt = re.search(r"type:\s*([A-Za-z]+)", block)
    if mt:
        slicer_type = mt.group(1)
    mw = re.search(r"width:\s*(\d+).*?height:\s*(\d+)", block, re.S)
    if mw:
        slicer_w, slicer_h = int(mw.group(1)), int(mw.group(2))

# overrides: collect any quoted visual names listed under an overrides: block
exempt = set()
mo = re.search(r"overrides:\s*\n((?:\s+.*\n)+)", text)
if mo:
    for nm in re.findall(r'visual:\s*"([^"]+)"', mo.group(1)):
        exempt.add(nm)

SLICER_FAMILY = {"slicer", "listSlicer", "advancedSlicerVisual", "textSlicer"}

# --- walk visuals ---------------------------------------------------------
findings = []  # (severity, page, name, msg)
pages_dir = os.path.join(report, "definition", "pages")
for root, _dirs, files in os.walk(pages_dir):
    if "visual.json" not in files:
        continue
    vj = os.path.join(root, "visual.json")
    try:
        d = json.load(open(vj, encoding="utf-8"))
    except Exception:
        continue
    page = os.path.basename(os.path.dirname(os.path.dirname(vj)))
    name = d.get("name", os.path.basename(os.path.dirname(vj)))
    if name in exempt:
        continue
    pos = d.get("position", {}) or {}
    vtype = (d.get("visual", {}) or {}).get("visualType", "")

    # sub-pixel + off-grid (all visuals)
    for k in ("x", "y", "width", "height"):
        v = pos.get(k)
        if v is None:
            continue
        if float(v) != int(v):
            findings.append(("SUBPIXEL", page, name, f"{k}={v} is not a whole number"))
        elif int(v) % snap != 0:
            findings.append(("OFFGRID", page, name, f"{k}={int(v)} not a multiple of {snap}"))

    # slicer-specific
    if vtype in SLICER_FAMILY:
        if vtype != slicer_type:
            findings.append(("SLICER_TYPE", page, name,
                             f"visualType '{vtype}' != design-system slicer type '{slicer_type}'"))
        if vtype == slicer_type and slicer_w is not None:
            w, h = pos.get("width"), pos.get("height")
            if w is not None and h is not None and (int(w) != slicer_w or int(h) != slicer_h):
                findings.append(("SLICER_SIZE", page, name,
                                 f"size {int(w)}x{int(h)} != design-system {slicer_w}x{slicer_h}"))

# --- report ---------------------------------------------------------------
out = sys.stderr if hook_mode else sys.stdout
if not findings:
    print(f"[layout-audit] OK - no drift vs {os.path.basename(yaml_path)}", file=out)
    sys.exit(0)

print(f"[layout-audit] {len(findings)} finding(s) vs {os.path.basename(yaml_path)} "
      f"(snap={snap}, slicer={slicer_type} {slicer_w}x{slicer_h}):", file=out)
for sev, page, name, msg in findings:
    print(f"  [{sev:11s}] {page}/{name}: {msg}", file=out)

sys.exit(2 if hook_mode else 0)
PYEOF
