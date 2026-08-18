"""Page 1 - Churn Overview. Where do we stand, and why did they leave?"""
from churnkit import (CHURNED, FACT, INK, INK2, RULE, SURFACE, add_page, head_tb, image_svg,
                      lit, noframe, page_chrome, proj_c, proj_m, rects, solid, stack, textbox,
                      ts, vis, write)

d = add_page("Overview", "Churn Overview")

page_chrome(d, "Churn Overview",
            "Where we stand at the end of Q2 2022 \u2014 and why customers left")

# ---- KPI row -------------------------------------------------------------
k = rects("kpi_hero_plus_4")


def kpi(name, rect, meas, title, colour=INK, size="28D", units=None, prec=None, note=None):
    head, body = stack(rect)
    if note:                       # hero reserves a footnote strip under the value
        body = dict(body, height=body["height"] - 40)   # snap-aligned footnote strip
    write(d, name + "H", head_tb(name + "H", head, title))
    props = {"color": solid(colour), "fontSize": lit(size),
             "fontFamily": lit("'Segoe UI Semibold'")}
    if units:
        props["labelDisplayUnits"] = lit(units)
    if prec is not None:
        props["labelPrecision"] = lit(prec)
    write(d, name, vis(name, "card", body, 200,
        query={"Values": {"projections": [proj_m(meas)]}},
        objects={"labels": [{"properties": props}],
                 "categoryLabels": [{"properties": {"show": lit("false")}}]}))
    if note:
        write(d, name + "N", textbox(name + "N",
            {"x": rect["x"], "y": body["y"] + body["height"] + 8,
             "width": rect["width"], "height": 32}, [(note, ts("9pt", INK2))]))


kpi("kpiRate", k[0], "Churn Rate", "Churn rate", CHURNED, "40D",
    note="1,869 of 6,589 churned or stayed \u00b7 26.5% if Joined are in the base")
kpi("kpiTotal",  k[1], "Total Customers",         "Customers")
kpi("kpiJoined", k[2], "Joined Customers",        "Joined this quarter")
kpi("kpiRev",    k[3], "Churned Revenue",         "Lifetime revenue lost", CHURNED,
    units="1000000D", prec="2D")
kpi("kpiRisk",   k[4], "Monthly Revenue at Risk", "Recurring $ / month",   CHURNED,
    units="1000D", prec="1D")

# ---- body ---------------------------------------------------------------
b = rects("overview_body")

h0, c0 = stack(b[0])          # no subtitle: the SVG already prints its own unit note
write(d, "waffleH", head_tb("waffleH", h0, "Customer status mix"))
write(d, "statusWaffle", image_svg("statusWaffle", c0, "Status Waffle"))

h1, c1 = stack(b[1], sub=True)
write(d, "catH", head_tb("catH", h1, "Why they left", "churned customers only"))
_cat = vis("categoryBar", "barChart", c1, 200,
    query={"Category": {"projections": [proj_c(FACT, "Churn Category")]},
           "Y": {"projections": [proj_m("Churned Customers")]}},
    objects={"dataPoint": [{"properties": {"fill": solid(CHURNED)}}],
             "categoryAxis": [{"properties": {"show": lit("true"), "showAxisTitle": lit("false"),
                                             "labelColor": solid(INK2), "fontSize": lit("9D")}}],
             "valueAxis": [{"properties": {"show": lit("false")}}],
             "labels": [{"properties": {"show": lit("true"), "color": solid(INK2),
                                        "fontSize": lit("9D")}}],
             "legend": [{"properties": {"show": lit("false")}}]})
_cat["visual"]["query"]["sortDefinition"] = {"sort": [{"field": {"Measure": {
    "Expression": {"SourceRef": {"Entity": "_Measures"}},
    "Property": "Churned Customers"}}, "direction": "Descending"}]}
write(d, "categoryBar", _cat)

h2, c2 = stack(b[2], sub=True)
write(d, "reasonH", head_tb("reasonH", h2, "Every churn reason, ranked",
                            "verbatim reason recorded at churn \u00b7 21 distinct \u00b7 "
                            "competitor-driven reasons are 45% of all churn"))
_rt = vis("reasonTable", "tableEx", c2, 200,
    query={"Values": {"projections": [
        proj_c(FACT, "Churn Reason", "Reason"),
        proj_c(FACT, "Churn Category", "Category"),
        proj_m("Churned Customers", "Customers"),
        proj_m("Churned Share of Total", "% of churn"),
        proj_m("Reason Bar", " ")]}},
    objects={"grid": [{"properties": {"imageHeight": lit("14D"), "imageWidth": lit("150D"),
                                      "gridVertical": lit("false"), "gridHorizontal": lit("true"),
                                      "gridHorizontalColor": solid(RULE),
                                      "outlineWeight": lit("0D"), "rowPadding": lit("3D")}}],
             "columnHeaders": [{"properties": {"fontColor": solid(INK2), "fontSize": lit("9D"),
                                               "backColor": solid(SURFACE)}}],
             "values": [{"properties": {"fontColor": solid(INK), "fontSize": lit("10D"),
                                        "backColorPrimary": solid(SURFACE),
                                        "backColorSecondary": solid(SURFACE)}}],
             "total": [{"properties": {"totals": lit("false")}}]})
_rt["visual"]["query"]["sortDefinition"] = {"sort": [{"field": {"Measure": {
    "Expression": {"SourceRef": {"Entity": "_Measures"}},
    "Property": "Churned Customers"}}, "direction": "Descending"}]}
write(d, "reasonTable", _rt)

print("page 1 built")
