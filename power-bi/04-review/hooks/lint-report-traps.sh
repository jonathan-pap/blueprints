#!/usr/bin/env bash
# lint-report-traps.sh - catch the render-time traps that `pbir validate` passes.
#
# The report-side counterpart to lint-tmdl-traps.sh. Every check here comes from an
# incident recorded in 02-build/report/validate/build-traps.md - things that are
# schema-valid and still ship wrong. Schema validation runs constantly and catches
# none of them; this is the check that earns its place.
#
# ERR (a defect, not a preference):
#   T1  default sort by MEASURE descending      - silently inverts a time series
#   T15 container title shown on a chart        - renders your title AND the auto title, stacked
#   T9  filterConfig nested inside `visual`     - belongs at the root of visual.json
#
# WARN (heuristic; check the render before acting):
#   T5  textbox font too large for its box      - text overflows, Power BI adds a scrollbar
#   T6  short slicer not in Dropdown mode       - renders a header and a sliver of one row
#   T6b slicer shows container title AND header - the field name renders twice, stacked
#   T14 horizontal bars under ~32px each        - chart scrolls, silently omitting categories
#   T11 multiple registered themes accumulating - `pbir theme build` does not remove the old one
#
# Usage:
#   bash lint-report-traps.sh "<project>.Report"           # manual: prints report, exit 0
#   bash lint-report-traps.sh --hook "<project>.Report"    # opt-in: findings -> stderr, exit 2 on ERR
#   bash lint-report-traps.sh --page Overview "<p>.Report" # one page - run after each page is built
#
# Run it per page during B10, not per file write: a page is the unit where a trap is
# both visible and cheap to fix. Full doctrine: ../../02-build/report/validate/build-traps.md
#
# Dependency-light: needs python (3.x) on PATH. Skips silently if absent.

set -u

HOOK_MODE=0
PAGE_FILTER=""
while [ $# -gt 0 ]; do
  case "${1:-}" in
    --hook) HOOK_MODE=1; shift ;;
    --page) PAGE_FILTER="${2:-}"; shift 2 ;;
    *) break ;;
  esac
done
REPORT="${1:-}"

if [ -z "$REPORT" ]; then
  echo "usage: lint-report-traps.sh [--hook] [--page <name>] <project>.Report" >&2
  exit 0
fi

PY=""
for c in python python3 py; do
  if command -v "$c" >/dev/null 2>&1 && "$c" -c "import sys" >/dev/null 2>&1; then PY="$c"; break; fi
done
[ -z "$PY" ] && exit 0   # no usable python -> skip silently

"$PY" - "$REPORT" "$HOOK_MODE" "$PAGE_FILTER" <<'PYEOF'
import json, os, sys, glob

report, hook_mode, page_filter = sys.argv[1], sys.argv[2] == "1", sys.argv[3]

pages_dir = os.path.join(report, "definition", "pages")
if not os.path.isdir(pages_dir):
    sys.exit(0)                      # not a PBIR report -> skip silently

# Visuals with a natural axis order, where a value-descending default sort rewrites the story.
CHART = {"barChart", "columnChart", "clusteredBarChart", "clusteredColumnChart",
         "stackedBarChart", "stackedColumnChart", "lineChart", "areaChart", "scatterChart",
         "donutChart", "pieChart", "waterfallChart", "lineClusteredColumnComboChart",
         "lineStackedColumnComboChart", "ribbonChart", "funnel"}
BAR = {"barChart", "clusteredBarChart", "stackedBarChart"}

def lit(props, key):
    """Read a PBIR literal property value, e.g. show -> 'true'."""
    try:
        return props[key]["expr"]["Literal"]["Value"].strip("'")
    except Exception:
        return None

findings = []          # (severity, page, visual, trap, message)

def add(sev, page, name, trap, msg):
    findings.append((sev, page, name, trap, msg))

for page_dir in sorted(glob.glob(os.path.join(pages_dir, "*"))):
    if not os.path.isdir(page_dir):
        continue
    page = os.path.basename(page_dir)
    pj = os.path.join(page_dir, "page.json")
    if os.path.isfile(pj):
        try:
            page = json.load(open(pj, encoding="utf-8")).get("displayName", page)
        except Exception:
            pass
    if page_filter and page_filter.lower() not in page.lower():
        continue

    for vf in sorted(glob.glob(os.path.join(page_dir, "visuals", "*", "visual.json"))):
        name = os.path.basename(os.path.dirname(vf))
        try:
            d = json.load(open(vf, encoding="utf-8"))
        except Exception:
            continue
        v = d.get("visual", {}) or {}
        vt = v.get("visualType", "") or ""
        pos = d.get("position", {}) or {}
        h = pos.get("height") or 0
        w = pos.get("width") or 0
        vco = v.get("visualContainerObjects", {}) or {}

        # --- T9: filterConfig must sit at the ROOT of visual.json, never inside `visual` ---
        if "filterConfig" in v:
            add("ERR", page, name, "T9",
                "filterConfig is nested inside `visual` - it belongs at the root of visual.json")

        # --- T1: the CLI's default sort, by measure, descending ---
        # Severity depends on the axis: on a time axis this inverts the story (ERR); on a plain
        # category it is merely implicit - right for a Pareto, an accident everywhere else (WARN).
        sd = (v.get("query", {}) or {}).get("sortDefinition", {}) or {}
        if sd.get("isDefaultSort") is True and vt in CHART:
            axis = ""
            for role in ("Category", "X", "Axis"):
                for p in ((v.get("query", {}).get("queryState", {}) or {})
                          .get(role, {}) or {}).get("projections", []) or []:
                    fld = p.get("field", {}) or {}
                    for kind in ("Column", "Measure", "HierarchyLevel"):
                        ref = fld.get(kind)
                        if isinstance(ref, dict):
                            ent = (ref.get("Expression", {}).get("SourceRef", {}) or {}).get("Entity", "")
                            axis = f"{ent}.{ref.get('Property', '')}"
            temporal = any(t in axis.lower() for t in
                           ("date", "month", "year", "quarter", "week", "day", "period", "time"))
            for s in sd.get("sort", []) or []:
                if "Measure" in (s.get("field", {}) or {}) and s.get("direction") == "Descending":
                    if temporal:
                        add("ERR", page, name, "T1",
                            f"{vt} on a time axis ({axis}) keeps the default measure-descending sort - "
                            f"the series renders in value order, so a growing trend can read as a decline. "
                            f"Sort on the axis column, Ascending, isDefaultSort:false")
                    else:
                        add("WARN", page, name, "T1",
                            f"{vt} sort is implicit (isDefaultSort:true, measure descending, axis {axis}) - "
                            f"correct for a Pareto, an accident anywhere else. Make it explicit "
                            f"(isDefaultSort:false) so it survives a CLI default change")

        # --- T15: a container title on a chart renders stacked with the auto title ---
        for tob in (vco.get("title") or []):
            props = tob.get("properties", {}) or {}
            show = lit(props, "show")
            if vt in CHART and (show == "true" or ("text" in props and show != "false")):
                add("ERR", page, name, "T15",
                    "container title is shown on a chart - Power BI renders it AND the auto title, "
                    "stacked; keep title show:false and use a textbox heading")

        # --- T6 / T6b: slicer sizing + duplicated header ---
        if "slicer" in vt.lower():
            mode = None
            for ob in ((v.get("objects", {}) or {}).get("data") or []):
                mode = lit(ob.get("properties", {}) or {}, "mode") or mode
            if h and h < 100 and mode != "Dropdown":
                add("WARN", page, name, "T6",
                    f"slicer is {int(h)}px tall in List mode - shows a header and a sliver of one row; "
                    f"use Dropdown mode or give it ~160px")
            header_shown = False
            for ob in ((v.get("objects", {}) or {}).get("header") or []):
                if lit(ob.get("properties", {}) or {}, "show") == "true":
                    header_shown = True
            for tob in (vco.get("title") or []):
                if lit(tob.get("properties", {}) or {}, "show") == "true" and header_shown:
                    add("WARN", page, name, "T6b",
                        "slicer shows both its container title and its own header - the field name "
                        "renders twice, one above the other")

        # --- T5: a textbox whose font cannot fit its box ---
        if vt in ("textbox", "textBox") and h:
            sizes = []
            def scan(o):
                if isinstance(o, dict):
                    for k, val in o.items():
                        if k in ("fontSize", "textSize") and isinstance(val, (int, float)):
                            sizes.append(val)
                        scan(val)
                elif isinstance(o, list):
                    for x in o:
                        scan(x)
            scan(v)
            if sizes and max(sizes) * 2.7 > h:
                add("WARN", page, name, "T5",
                    f"{int(max(sizes))}pt text in a {int(h)}px box - likely overflows and adds a "
                    f"scrollbar; ~16pt fits 48px")

        # --- T14: horizontal bars need ~32px each or the chart scrolls silently ---
        if vt in BAR and h:
            topn = None
            for fc in (d.get("filterConfig", {}) or {}).get("filters", []) or []:
                try:
                    n = fc["filter"]["Where"][0]["Condition"]["TopN"]["ItemCount"]
                    topn = max(topn or 0, int(n))
                except Exception:
                    pass
            if topn and h / topn < 32:
                add("WARN", page, name, "T14",
                    f"top-{topn} bars in {int(h)}px = {h/topn:.0f}px each - under ~32px the chart "
                    f"scrolls and silently omits the last categories the title promises")

# --- T11: registered themes accumulate; pbir theme build does not remove the old one ---
rr = os.path.join(report, "StaticResources", "RegisteredResources")
if os.path.isdir(rr):
    themes = [f for f in os.listdir(rr) if f.lower().endswith(".json")]
    if len(themes) > 1:
        add("WARN", "(report)", "StaticResources", "T11",
            f"{len(themes)} registered themes present - `pbir theme build` leaves the previous one "
            f"behind; dead themes ship with the report")

out = sys.stderr if hook_mode else sys.stdout
scope = f" [page: {page_filter}]" if page_filter else ""
if not findings:
    print(f"[trap-lint] OK - no build traps in {os.path.basename(report)}{scope}", file=out)
    sys.exit(0)

errs = [f for f in findings if f[0] == "ERR"]
print(f"[trap-lint] {len(findings)} finding(s) in {os.path.basename(report)}{scope} "
      f"({len(errs)} ERR) - see 02-build/report/validate/build-traps.md", file=out)
for sev, page, name, trap, msg in findings:
    print(f"  [{sev:4s}] {trap:4s} {page}/{name}: {msg}", file=out)

sys.exit(2 if (hook_mode and errs) else 0)
PYEOF
