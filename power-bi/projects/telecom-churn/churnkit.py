"""Page/visual builder for the churn report. All geometry comes from design-system.yaml."""
import json
import os
import shutil
import subprocess
import sys

import resolve_layout as RL

ROOT = os.path.dirname(os.path.abspath(__file__))
REPORT = os.path.join(ROOT, "telecom-churn.Report")
PAGES = os.path.join(REPORT, "definition", "pages")
SCHEMA = ("https://developer.microsoft.com/json-schemas/fabric/item/report/"
          "definition/visualContainer/2.10.0/schema.json")
FACT = "telecom_customer_churn"

INK, INK2, INK3 = "#1B1F27", "#5B6472", "#7A8494"
CHURNED, STAYED, JOINED = "#B8480A", "#00558F", "#B673A4"
SURFACE, RULE, CANVAS = "#FFFFFF", "#DCE1E9", "#EEF1F5"

DS = RL.load(os.path.join(ROOT, RL.DS))


def rects(layout_name):
    return RL.layout(layout_name, DS)


def lit(v):
    return {"expr": {"Literal": {"Value": v}}}


def solid(c):
    return {"solid": {"color": lit("'%s'" % c)}}


def measure(name):
    return {"Measure": {"Expression": {"SourceRef": {"Entity": "_Measures"}}, "Property": name}}


def col(entity, prop):
    return {"Column": {"Expression": {"SourceRef": {"Entity": entity}}, "Property": prop}}


def proj_m(name, disp=None):
    p = {"field": measure(name), "queryRef": "_Measures." + name, "nativeQueryRef": name}
    if disp:
        p["displayName"] = disp
    return p


def proj_c(entity, prop, disp=None):
    p = {"field": col(entity, prop), "queryRef": "%s.%s" % (entity, prop), "nativeQueryRef": prop}
    if disp:
        p["displayName"] = disp
    return p


def run(*a):
    p = subprocess.run(a, cwd=ROOT, capture_output=True, text=True)
    out = (p.stdout or "").strip()
    if out:
        print("  " + out[:200])
    if p.returncode:
        print("  ERR:", (p.stderr or "").strip()[:200])
    return p.returncode


def add_page(pid, display, w=1280, h=720):
    before = set(os.listdir(PAGES))
    if run("pbir", "add", "page", "telecom-churn.Report/%s.Page" % display, "-n", display):
        sys.exit("add page failed: " + display)
    new = sorted(set(os.listdir(PAGES)) - before)
    run("pbir", "pages", "rename", "telecom-churn.Report/%s.Page" % display, "--to", pid, "-f")
    d = os.path.join(PAGES, pid)
    if not os.path.isdir(d):
        d = os.path.join(PAGES, new[0])
    pj = os.path.join(d, "page.json")
    pg = json.load(open(pj, encoding="utf-8"))
    old = pg["name"]
    pg["name"], pg["displayName"] = pid, display
    pg["width"], pg["height"] = w, h
    pg["displayOption"] = "FitToPage"
    json.dump(pg, open(pj, "w", encoding="utf-8", newline="\n"), indent=2)
    meta_p = os.path.join(PAGES, "pages.json")
    meta = json.load(open(meta_p, encoding="utf-8"))
    meta["pageOrder"] = [pid if x == old else x for x in meta["pageOrder"]]
    if pid not in meta["pageOrder"]:
        meta["pageOrder"].append(pid)
    meta["activePageName"] = meta["pageOrder"][0]
    json.dump(meta, open(meta_p, "w", encoding="utf-8", newline="\n"), indent=2)
    # remove the auto Title textbox
    vd = os.path.join(d, "visuals")
    for x in list(os.listdir(vd)) if os.path.isdir(vd) else []:
        v = json.load(open(os.path.join(vd, x, "visual.json"), encoding="utf-8"))
        if v.get("visual", {}).get("visualType") == "textbox":
            shutil.rmtree(os.path.join(vd, x))
    print("  page %s (%dx%d)" % (pid, w, h))
    return d


def write(page_dir, name, obj):
    d = os.path.join(page_dir, "visuals", name)
    os.makedirs(d, exist_ok=True)
    json.dump(obj, open(os.path.join(d, "visual.json"), "w", encoding="utf-8", newline="\n"),
              indent=2)


def vis(name, vtype, rect, z, query=None, objects=None, vco=None, tab=1):
    v = {"visualType": vtype}
    if query is not None:
        v["query"] = {"queryState": query}
    v["objects"] = objects or {}
    v["visualContainerObjects"] = vco if vco is not None else {}
    v["drillFilterOtherVisuals"] = True
    return {"$schema": SCHEMA, "name": name,
            "position": {"x": rect["x"], "y": rect["y"], "z": z,
                         "width": rect["width"], "height": rect["height"], "tabOrder": tab},
            "visual": v}


def textbox(name, rect, runs, z=900):
    paras = [{"textRuns": [{"value": v, "textStyle": s}]} for v, s in runs]
    return vis(name, "textbox", rect, z,
               query={}, objects={"general": [{"properties": {"paragraphs": paras}}]},
               vco=noframe())


def ts(size, colour=INK, face="Segoe UI"):
    return {"fontFamily": face, "fontSize": size, "color": colour}


def noframe():
    off = [{"properties": {"show": lit("false")}}]
    return {"title": off, "background": off, "border": off}


def panel():
    """Card chrome. The container TITLE is always off: setting title.text on a chart makes
    Power BI render the custom title AND its auto-generated name ("Churned Customers by
    Churn Category") stacked. Every heading is a textbox instead - deterministic, and it is
    the pattern the rest of the workspace already uses."""
    return {"title": [{"properties": {"show": lit("false")}}],
            "background": [{"properties": {"show": lit("true"), "color": solid(SURFACE),
                                           "transparency": lit("0D")}}],
            "border": [{"properties": {"show": lit("true"), "color": solid(RULE),
                                       "radius": lit("6D")}}]}


def heading(name, rect, title, sub=None, pad=14, z=950):
    """Heading textbox pinned inside a panel's top edge."""
    runs = [(title, ts("11pt", INK, "Segoe UI Semibold"))]
    if sub:
        runs.append((sub, ts("9pt", INK2)))
    h = 44 if sub else 26
    return textbox(name, {"x": rect["x"] + pad, "y": rect["y"] + 8,
                          "width": rect["width"] - 2 * pad, "height": h}, runs, z=z)


def inset(rect, top=38, pad=8, bottom=8):
    """Content rect inside a panel, below its heading."""
    return {"x": rect["x"] + pad, "y": rect["y"] + top,
            "width": rect["width"] - 2 * pad, "height": rect["height"] - top - bottom}


def image_svg(name, rect, measure_name, z=100):
    return vis(name, "image", rect, z,
               objects={"image": [{"properties": {
                   "sourceType": lit("'imageData'"), "transparency": lit("0D"),
                   "effects": lit("false"), "fit": lit("'Fit'"),
                   "sourceField": {"expr": measure(measure_name)}}}]},
               vco=noframe())

def stack(rect, sub=False, gap=8):
    """Split a region into a heading strip (on the canvas) and a content rect below it.

    Panels-as-shapes were abandoned: a shape visual would not render its fill even with
    objects.fill set explicitly. Every content visual instead carries its OWN themed white
    card (theme `*` sets background + border), and the heading sits above it on the canvas.
    Fewer visuals, nothing to keep in sync, and no z-order to reason about.
    """
    # heading heights and the gap are all multiples of the 8px snap, so the derived content
    # rect stays on-grid - the audit caught 44 off-snap coordinates when gap was 6
    h = 40 if sub else 24
    head = {"x": rect["x"], "y": rect["y"], "width": rect["width"], "height": h}
    body = {"x": rect["x"], "y": rect["y"] + h + gap,
            "width": rect["width"], "height": rect["height"] - h - gap}
    return head, body


def head_tb(name, rect, title, sub=None):
    runs = [(title, ts("11pt", INK, "Segoe UI Semibold"))]
    if sub:
        runs.append((sub, ts("9pt", INK2)))
    return textbox(name, rect, runs, z=900)
