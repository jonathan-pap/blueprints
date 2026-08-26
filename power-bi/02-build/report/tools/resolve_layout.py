"""Resolve design-system.yaml regions to pixel rectangles (ROOM TOOL - shared by every project).

Every visual position comes from here - nothing is hardcoded at a call site. Cell math per
../layout/layout-guidelines.md#grid-12x12. Projects do NOT copy this file; they import it:

    sys.path.insert(0, "<workspace>/power-bi/02-build/report/tools"); import resolve_layout as RL
    DS = RL.load("projects/<name>/design-system.yaml"); RL.layout("kpi_row_4", DS)

CLI:  python resolve_layout.py [path/to/design-system.yaml] [layout ...]

Regions are [col_start, row_start, col_end, row_end], 1-indexed, END-EXCLUSIVE.
Region EDGES are snapped to the grid snap (8px), then width/height derive from the snapped
edges - so adjacent regions still tile exactly instead of drifting apart by a rounding each.
"""
import json
import sys

import yaml

DS = "design-system.yaml"


def load(path=DS):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def cells(ds):
    g, p = ds["grid"], ds["meta"]["page"]
    colW = (p["width"] - 2 * g["margin"] - g["gutter"] * (g["columns"] - 1)) / g["columns"]
    rowH = (p["height"] - 2 * g["margin"] - g["gutter"] * (g["rows"] - 1)) / g["rows"]
    return colW, rowH


def _snap(v, s):
    return int(s * round(v / s))


def region_px(ds, region):
    g = ds["grid"]
    colW, rowH = cells(ds)
    m, gut, snap = g["margin"], g["gutter"], g["snap"]
    c1, r1, c2, r2 = region
    x1 = _snap(m + (c1 - 1) * (colW + gut), snap)
    x2 = _snap(m + (c2 - 1) * (colW + gut) - gut, snap)
    y1 = _snap(m + (r1 - 1) * (rowH + gut), snap)
    y2 = _snap(m + (r2 - 1) * (rowH + gut) - gut, snap)
    return {"x": x1, "y": y1, "width": x2 - x1, "height": y2 - y1}


def layout(name, ds=None):
    ds = ds or load()
    return [region_px(ds, r) for r in ds["layouts"][name]]


if __name__ == "__main__":
    args = sys.argv[1:]
    path = args.pop(0) if args and args[0].endswith((".yaml", ".yml")) else DS
    ds = load(path)
    colW, rowH = cells(ds)
    pg = ds["meta"]["page"]
    print("page %dx%d  colW=%.2f rowH=%.2f" % (pg["width"], pg["height"], colW, rowH))
    names = args or list(ds["layouts"])
    for n in names:
        print("\n%s:" % n)
        for r in layout(n, ds):
            print("   x=%(x)-5d y=%(y)-5d w=%(width)-5d h=%(height)-5d" % r)
