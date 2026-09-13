"""pbirkit - the shared PBIR authoring core (ROOM TOOL - one copy, every project imports it).

Builds page/visual JSON for a PBIR report from design-system.yaml regions. Everything that
earned its place across the telecom-churn and arcane-emporium builds lives here once:
headings as textboxes, panels via the theme (not shape visuals), slicers with syncGroup,
projection/literal helpers, page creation through `pbir`, and on-snap region stacking.

A project kit (projects/<name>/<name>kit.py) holds ONLY what is project-specific - palette,
the fact/measure table names, and bespoke visual recipes - and configures this module:

    import os, sys
    ROOT = os.path.dirname(os.path.abspath(__file__))
    WS = os.path.normpath(os.path.join(ROOT, "..", "..", "02-build", "report"))
    sys.path.insert(0, os.path.join(WS, "tools"))
    import pbirkit as K
    K.configure(root=ROOT, report="<name>.Report", fact="FactSales",
                palette=dict(INK="#0B1020", INK2="#4A5578", INK3="#6E7A9C",
                             SURFACE="#FFFFFF", RULE="#DEE4F2", CANVAS="#F1F4FB"))
    from pbirkit import *     # AFTER configure, so DS/PAGES/palette names bind to real values

Functions read module globals at CALL time, so configure() must run before any call.
Geometry: ./resolve_layout.py. Conventions: ../schema-patterns/, ../add-visual/.
"""
import json
import os
import shutil
import subprocess
import sys

import resolve_layout as RL

SCHEMA = ("https://developer.microsoft.com/json-schemas/fabric/item/report/"
          "definition/visualContainer/2.10.0/schema.json")
Q = chr(39)

# ---- configured per project (see configure) ----------------------------------------
ROOT = REPORT = PAGES = None
FACT = None
M = "_Measures"
DS = None
# neutral light palette defaults; projects override via configure(palette=...)
INK, INK2, INK3 = "#0B1020", "#4A5578", "#6E7A9C"
SURFACE, RULE, CANVAS = "#FFFFFF", "#DEE4F2", "#F1F4FB"


def configure(root, report, fact=None, measures_table="_Measures", palette=None,
              ds_path=None, schema=None):
    """Bind the kit to one project. `report` is the .Report folder name; `root` its parent."""
    g = globals()
    g["ROOT"] = root
    g["REPORT"] = os.path.join(root, report)
    g["PAGES"] = os.path.join(g["REPORT"], "definition", "pages")
    g["FACT"] = fact
    g["M"] = measures_table
    if schema:
        g["SCHEMA"] = schema
    if palette:
        for k, v in palette.items():
            g[k] = v
    g["DS"] = RL.load(ds_path or os.path.join(root, RL.DS))
    return g["DS"]


def _report_name():
    return os.path.basename(REPORT)


# ---- geometry ------------------------------------------------------------------------
def rects(layout_name):
    """Pixel rects for a named layouts: entry in design-system.yaml."""
    return RL.layout(layout_name, DS)


def stack(rect, sub=False, gap=8):
    """Split a region into a heading strip (on the canvas) and a content rect below it.

    Panels-as-shapes were abandoned: a shape visual would not render its fill even with
    objects.fill set. Every content visual carries its OWN themed card (theme `*` sets
    background + border) and the heading sits above it. Heading heights and the gap are
    multiples of the 8px snap so the derived content rect stays on-grid.
    """
    h = 40 if sub else 24
    head = {"x": rect["x"], "y": rect["y"], "width": rect["width"], "height": h}
    body = {"x": rect["x"], "y": rect["y"] + h + gap,
            "width": rect["width"], "height": rect["height"] - h - gap}
    return head, body


def inset(rect, top=38, pad=8, bottom=8):
    """Content rect inside a panel, below its heading."""
    return {"x": rect["x"] + pad, "y": rect["y"] + top,
            "width": rect["width"] - 2 * pad, "height": rect["height"] - top - bottom}


# ---- expression + projection helpers -----------------------------------------------
def lit(v):
    return {"expr": {"Literal": {"Value": v}}}


def solid(c):
    return {"solid": {"color": lit("'%s'" % c)}}


def measure(name, entity=None):
    return {"Measure": {"Expression": {"SourceRef": {"Entity": entity or M}}, "Property": name}}


def col(entity, prop):
    return {"Column": {"Expression": {"SourceRef": {"Entity": entity}}, "Property": prop}}


def proj_m(name, disp=None, entity=None):
    e = entity or M
    p = {"field": measure(name, e), "queryRef": e + "." + name, "nativeQueryRef": name}
    if disp:
        p["displayName"] = disp
    return p


def proj_c(entity, prop, disp=None):
    p = {"field": col(entity, prop), "queryRef": "%s.%s" % (entity, prop), "nativeQueryRef": prop}
    if disp:
        p["displayName"] = disp
    return p


def ts(size, colour=None, face="Segoe UI"):
    return {"fontFamily": face, "fontSize": size, "color": colour or INK}


def sort_by(v, field, direction="Descending"):
    """sortDefinition is a SIBLING of queryState, not inside it."""
    v["visual"]["query"]["sortDefinition"] = {"sort": [{"field": field, "direction": direction}]}
    return v


def axis(show=True, colour=None, extra=None):
    p = {"show": lit("true" if show else "false"), "showAxisTitle": lit("false"),
         "labelColor": solid(colour or INK3), "fontSize": lit("9D"), "gridlineShow": lit("false")}
    if extra:
        p.update(extra)
    return [{"properties": p}]


def in_filter(entity, prop, values, fname):
    """Categorical In-filter over several values of one column (visual filterConfig entry)."""
    src = {"Column": {"Expression": {"SourceRef": {"Source": "f"}}, "Property": prop}}
    return {"name": fname,
            "field": {"Column": {"Expression": {"SourceRef": {"Entity": entity}},
                                 "Property": prop}},
            "type": "Categorical",
            "filter": {"Version": 2,
                       "From": [{"Name": "f", "Entity": entity, "Type": 0}],
                       "Where": [{"Condition": {"In": {
                           "Expressions": [src],
                           "Values": [[{"Literal": {"Value": Q + v + Q}}] for v in values]}}}]},
            "howCreated": "User"}


# ---- container chrome ----------------------------------------------------------------
def noframe():
    off = [{"properties": {"show": lit("false")}}]
    return {"title": off, "background": off, "border": off}


def panel():
    """Card chrome. The container TITLE is always off: setting title.text on a chart makes
    Power BI render the custom title AND its auto-generated name stacked. Every heading is a
    textbox instead - deterministic, and the pattern the rest of the workspace uses."""
    return {"title": [{"properties": {"show": lit("false")}}],
            "background": [{"properties": {"show": lit("true"), "color": solid(SURFACE),
                                           "transparency": lit("0D")}}],
            "border": [{"properties": {"show": lit("true"), "color": solid(RULE),
                                       "radius": lit("6D")}}]}


# ---- visuals -------------------------------------------------------------------------
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


def head_tb(name, rect, title, sub=None):
    runs = [(title, ts("11pt", INK, "Segoe UI Semibold"))]
    if sub:
        runs.append((sub, ts("9pt", INK2)))
    return textbox(name, rect, runs, z=900)


def heading(name, rect, title, sub=None, pad=14, z=950):
    """Heading textbox pinned inside a panel's top edge."""
    runs = [(title, ts("11pt", INK, "Segoe UI Semibold"))]
    if sub:
        runs.append((sub, ts("9pt", INK2)))
    h = 44 if sub else 26
    return textbox(name, {"x": rect["x"] + pad, "y": rect["y"] + 8,
                          "width": rect["width"] - 2 * pad, "height": h}, runs, z=z)


def image_svg(name, rect, measure_name, z=100):
    """Image visual bound to an SVG data-URI measure (see ../../visuals/svg/)."""
    return vis(name, "image", rect, z,
               objects={"image": [{"properties": {
                   "sourceType": lit("'imageData'"), "transparency": lit("0D"),
                   "effects": lit("false"), "fit": lit("'Fit'"),
                   "sourceField": {"expr": measure(measure_name)}}}]},
               vco=noframe())


def register_image(item_name, content):
    """Package a static image INTO the report (StaticResources/RegisteredResources) and list it in
    report.json. Idempotent: rewrites the file, adds the registration once. For report chrome that
    isn't data - a literal data: URL in an image's imageUrl does NOT render (broken-image icon,
    verified 2026-09-13), so a fixed image has to be a registered resource."""
    rr = os.path.join(REPORT, "StaticResources", "RegisteredResources")
    os.makedirs(rr, exist_ok=True)
    mode = "wb" if isinstance(content, bytes) else "w"
    with open(os.path.join(rr, item_name), mode, **({} if mode == "wb" else {"encoding": "utf-8", "newline": "\n"})) as f:
        f.write(content)
    rp = os.path.join(REPORT, "definition", "report.json")
    rep = json.load(open(rp, encoding="utf-8"))
    pkgs = rep.setdefault("resourcePackages", [])
    pkg = next((p for p in pkgs if p.get("name") == "RegisteredResources"), None)
    if pkg is None:
        pkg = {"name": "RegisteredResources", "type": "RegisteredResources", "items": []}
        pkgs.append(pkg)
    if not any(i.get("name") == item_name for i in pkg["items"]):
        pkg["items"].append({"name": item_name, "path": item_name, "type": "Image"})
        json.dump(rep, open(rp, "w", encoding="utf-8", newline="\n"), indent=2)


def register_theme(theme_path):
    """Make a theme JSON the report's custom theme: copy it into RegisteredResources, list it as a
    CustomTheme resource, and point themeCollection.customTheme at it. Idempotent. Shape from the room
    example K201-MonthSlicer.Report. pbir 0.9.32 has no `theme apply <file>` (only apply-template), so
    this writes the PBIR directly - the tool-independent route (file-map.md)."""
    item = os.path.basename(theme_path)
    rr = os.path.join(REPORT, "StaticResources", "RegisteredResources")
    os.makedirs(rr, exist_ok=True)
    shutil.copyfile(theme_path, os.path.join(rr, item))
    rp = os.path.join(REPORT, "definition", "report.json")
    rep = json.load(open(rp, encoding="utf-8"))
    pkgs = rep.setdefault("resourcePackages", [])
    pkg = next((p for p in pkgs if p.get("name") == "RegisteredResources"), None)
    if pkg is None:
        pkg = {"name": "RegisteredResources", "type": "RegisteredResources", "items": []}
        pkgs.append(pkg)
    if not any(i.get("name") == item for i in pkg["items"]):
        pkg["items"].append({"name": item, "path": item, "type": "CustomTheme"})
    tc = rep.setdefault("themeCollection", {})
    base = tc.get("baseTheme", {}).get("reportVersionAtImport")
    tc["customTheme"] = {"name": item,
                         "reportVersionAtImport": base or {"visual": "2.12.0", "report": "3.4.0", "page": "2.3.1"},
                         "type": "RegisteredResources"}
    json.dump(rep, open(rp, "w", encoding="utf-8", newline="\n"), indent=2)


def unregister_image(item_name):
    """Remove a registered image - the file and its report.json entry. Idempotent. Use when a page
    is retired, or the resource lingers and ships with the report."""
    rr = os.path.join(REPORT, "StaticResources", "RegisteredResources", item_name)
    if os.path.isfile(rr):
        os.remove(rr)
    rp = os.path.join(REPORT, "definition", "report.json")
    rep = json.load(open(rp, encoding="utf-8"))
    for pkg in rep.get("resourcePackages", []):
        if pkg.get("name") == "RegisteredResources":
            kept = [i for i in pkg["items"] if i.get("name") != item_name]
            if len(kept) != len(pkg["items"]):
                pkg["items"] = kept
                json.dump(rep, open(rp, "w", encoding="utf-8", newline="\n"), indent=2)


def image_resource(name, rect, item_name, alt, z=100, tab=1):
    """Image visual showing a registered resource (see register_image). Binding shape from the
    room template ../examples/visuals/default/image.json. Data-driven images use image_svg()."""
    vco = noframe()
    vco["general"] = [{"properties": {"altText": lit("'%s'" % alt.replace("'", "''"))}}]
    # transparency + effects must be explicit: left unset, the image visual rendered the resource at
    # roughly 8% opacity (brightest gold pixel 18,20,23 instead of 232,195,73) - verified 2026-09-13.
    return vis(name, "image", rect, z,
               objects={"general": [{"properties": {"imageUrl": {"expr": {"ResourcePackageItem": {
                   "PackageName": "RegisteredResources", "PackageType": 1, "ItemName": item_name}}}}}],
                        "image": [{"properties": {"transparency": lit("0D"), "effects": lit("false")}}]},
               vco=vco, tab=tab)


def nav_button(name, rect, target_page, tooltip, z=500, tab=1, hover=None, hover_transparency=88):
    """A transparent PageNavigation button laid over artwork: invisible at rest, a faint wash on
    hover. The artwork carries the look; the button carries the click, keyboard focus and tooltip.
    `target_page` is the page NAME (its folder id), not the display name."""
    off = [{"properties": {"show": lit("false")}}]
    fill = [{"properties": {"show": lit("true")}},
            {"selector": {"id": "default"},
             "properties": {"fillColor": solid("#000000"), "transparency": lit("100D")}}]
    if hover:
        fill.append({"selector": {"id": "hover"},
                     "properties": {"fillColor": solid(hover),
                                    "transparency": lit("%dD" % hover_transparency)}})
    vco = noframe()
    vco["visualLink"] = [{"properties": {
        "show": lit("true"), "type": lit("'PageNavigation'"),
        "navigationSection": lit("'%s'" % target_page),
        "tooltip": lit("'%s'" % tooltip.replace("'", "''"))}}]
    return vis(name, "actionButton", rect, z,
               objects={"icon": off, "outline": off, "text": off, "fill": fill},
               vco=vco, tab=tab)


def slicer(name, rect, prop, group, tab=1, entity=None):
    """Dropdown slicer on entity.prop (entity defaults to the configured FACT), synced across
    pages via syncGroup - a SIBLING of visualType, not an object. Without it every page keeps
    its own selection and a cross-page comparison silently lies (references/anti-patterns.md)."""
    proj = proj_c(entity or FACT, prop)
    proj["active"] = True
    v = vis(name, "slicer", rect, 800,
            query={"Values": {"projections": [proj]}},
            objects={"data": [{"properties": {"mode": lit(Q + "Dropdown" + Q)}}]},
            vco={"title": [{"properties": {"show": lit("false")}}]}, tab=tab)
    v["visual"]["syncGroup"] = {"groupName": group, "fieldChanges": True, "filterChanges": True}
    return v


# ---- pages + files -------------------------------------------------------------------
def run(*a):
    """Run a CLI (pbir, powerbi-desktop...) from the project root; print a short tail."""
    p = subprocess.run(a, cwd=ROOT, capture_output=True, text=True)
    out = (p.stdout or "").strip()
    if out:
        print("  " + out[:200])
    if p.returncode:
        print("  ERR:", (p.stderr or "").strip()[:200])
    return p.returncode


def add_page(pid, display, w=1280, h=720):
    """Create a page via `pbir add page`, rename its folder to `pid`, normalise pages.json
    (drops phantom entries with no folder) and strip the auto Title textbox."""
    rep = _report_name()
    before = set(os.listdir(PAGES))
    if run("pbir", "add", "page", "%s/%s.Page" % (rep, display), "-n", display):
        sys.exit("add page failed: " + display)
    new = sorted(set(os.listdir(PAGES)) - before)
    run("pbir", "pages", "rename", "%s/%s.Page" % (rep, display), "--to", pid, "-f")
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
    live = set(os.listdir(PAGES))
    meta["pageOrder"] = [x for x in meta["pageOrder"] if x in live]
    meta["activePageName"] = meta["pageOrder"][0]
    json.dump(meta, open(meta_p, "w", encoding="utf-8", newline="\n"), indent=2)
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


__all__ = [n for n in dir() if not n.startswith("_") and n not in
           ("json", "os", "shutil", "subprocess", "sys", "RL")]
