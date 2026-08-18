"""Pages 2-4: Customer Profile, Churn Drivers, High-Value at Risk."""
from churnkit import (CHURNED, FACT, INK, INK2, RULE, STAYED, SURFACE, add_page, head_tb, lit,
                      measure, proj_c, proj_m, rects, solid, stack, textbox, ts, vis, write)

ATTR = "ProfileAttr"
Q = chr(39)
GRID = {"gridVertical": lit("false"), "gridHorizontal": lit("true"),
        "gridHorizontalColor": solid(RULE), "outlineWeight": lit("0D"), "rowPadding": lit("3D")}
HDRS = [{"properties": {"fontColor": solid(INK2), "fontSize": lit("9D"),
                        "backColor": solid(SURFACE)}}]
VALS = [{"properties": {"fontColor": solid(INK), "fontSize": lit("10D"),
                        "backColorPrimary": solid(SURFACE),
                        "backColorSecondary": solid(SURFACE)}}]
NOTOT = [{"properties": {"totals": lit("false")}}]


def table(name, rect, projections, grid_extra=None, z=200):
    g = dict(GRID)
    if grid_extra:
        g.update(grid_extra)
    return vis(name, "tableEx", rect, z,
               query={"Values": {"projections": projections}},
               objects={"grid": [{"properties": g}], "columnHeaders": HDRS,
                        "values": VALS, "total": NOTOT})


def sort_by(v, field, direction="Ascending"):
    v["visual"]["query"]["sortDefinition"] = {"sort": [{"field": field, "direction": direction}]}
    return v


def colref(entity, prop):
    return {"Column": {"Expression": {"SourceRef": {"Entity": entity}}, "Property": prop}}


def mref(name):
    return {"Measure": {"Expression": {"SourceRef": {"Entity": "_Measures"}}, "Property": name}}


def bars(name, rect, cat_entity, cat_col, meas, colour=CHURNED, z=200,
         fill_measure=None, sort_field=None, sort_dir="Descending"):
    dp = [{"properties": {"fill": solid(colour)}}]
    if fill_measure:
        dp.append({"properties": {"fill": {"solid": {"color": {"expr": measure(fill_measure)}}}},
                   "selector": {"data": [{"dataViewWildcard": {"matchingOption": 1}}]}})
    v = vis(name, "barChart", rect, z,
            query={"Category": {"projections": [proj_c(cat_entity, cat_col)]},
                   "Y": {"projections": [proj_m(meas)]}},
            objects={"dataPoint": dp,
                     "categoryAxis": [{"properties": {
                         "show": lit("true"), "showAxisTitle": lit("false"),
                         "labelColor": solid(INK2), "fontSize": lit("9D")}}],
                     "valueAxis": [{"properties": {"show": lit("false")}}],
                     "labels": [{"properties": {"show": lit("true"),
                                                "color": solid(INK2), "fontSize": lit("9D"),
                                                "labelPosition": lit("'OutsideEnd'")}}],
                     "legend": [{"properties": {"show": lit("false")}}]})
    if sort_field:
        sort_by(v, sort_field, sort_dir)
    return v


def cat_filter(fname, prop, value):
    return {"name": fname, "field": colref(FACT, prop), "type": "Categorical",
            "filter": {"Version": 2, "From": [{"Name": "f", "Entity": FACT, "Type": 0}],
                       "Where": [{"Condition": {"In": {
                           "Expressions": [{"Column": {
                               "Expression": {"SourceRef": {"Source": "f"}}, "Property": prop}}],
                           "Values": [[{"Literal": {"Value": Q + value + Q}}]]}}}]},
            "howCreated": "User"}


def topn_filter(entity, prop, meas, n, fname):
    """TopN visual filter. Shape lifted from a working example rather than invented: it is a
    SUBQUERY in From, selecting the column ordered by the measure with a Top, then an In
    against that subquery. 'itemCount'/'topBottom' properties are NOT valid here."""
    colsrc = {"Column": {"Expression": {"SourceRef": {"Source": "d"}}, "Property": prop}}
    return {
        "name": fname,
        "field": colref(entity, prop),
        "type": "TopN",
        "filter": {
            "Version": 2,
            "From": [
                {"Name": "subquery", "Type": 2, "Expression": {"Subquery": {"Query": {
                    "Version": 2,
                    "From": [{"Name": "d", "Entity": entity, "Type": 0},
                             {"Name": "f", "Entity": "_Measures", "Type": 0}],
                    "Select": [dict(colsrc, Name="field")],
                    "OrderBy": [{"Direction": 2, "Expression": {"Measure": {
                        "Expression": {"SourceRef": {"Source": "f"}}, "Property": meas}}}],
                    "Top": n,
                }}}},
                {"Name": "d", "Entity": entity, "Type": 0},
            ],
            "Where": [{"Condition": {"In": {
                "Expressions": [colsrc],
                "Table": {"SourceRef": {"Source": "subquery"}}}}}],
        },
        "howCreated": "User",
    }


HD = rects("header")[0]

# ======================================================= PAGE 2
d = add_page("Profile", "Customer Profile")
write(d, "pageTitle", textbox("pageTitle", HD, [
    ("Customer Profile", ts("20pt", INK, "Segoe UI Semibold")),
    ("Churned vs Stayed vs Joined - where the three groups actually differ", ts("10pt", INK2))]))

s = rects("profile_summary")[0]
h, c = stack(s)
write(d, "sumH", head_tb("sumH", h, "The three groups at a glance"))
write(d, "sumTable", sort_by(table("sumTable", c, [
    proj_c(FACT, "Customer Status", "Status"),
    proj_m("Total Customers", "Customers"),
    proj_m("Avg Tenure", "Avg tenure (mo)"),
    proj_m("Avg Monthly Charge", "Avg monthly $"),
    proj_m("Pct Month to Month", "On month-to-month"),
]), mref("Total Customers"), "Descending"))

b = rects("profile_body")[0]
h, c = stack(b, sub=True)
write(d, "divH", head_tb("divH", h, "Profile comparison - share within each status group",
                         "read ACROSS a row, never down a column \u00b7 blue dot = stayers, "
                         "vermillion = churners \u00b7 divergence is churned minus stayed, in pp"))
write(d, "divTable", sort_by(table("divTable", c, [
    proj_c(ATTR, "Attribute"),
    proj_c(ATTR, "Value"),
    proj_m("Attr Churn Share", "Churn"),
    proj_m("Attr Stay Share", "Stay"),
    proj_m("Attr Join Share", "Join"),
    proj_m("Attr Dumbbell", "stay - churn"),
    proj_m("Attr Divergence", "Diverg."),
], grid_extra={"imageHeight": lit("18D"), "imageWidth": lit("230D")}),
    colref(ATTR, "SortKey"), "Ascending"))

# ======================================================= PAGE 3
d = add_page("Drivers", "Churn Drivers")
write(d, "pageTitle", textbox("pageTitle", HD, [
    ("Churn Drivers", ts("20pt", INK, "Segoe UI Semibold")),
    ("Churn RATE by segment, ranked against the 28.4% baseline - rate not count, because a big "
     "segment churns more simply by being big", ts("10pt", INK2))]))

hero = rects("drivers_hero")[0]
h, c = stack(hero, sub=True)
write(d, "tornH", head_tb("tornH", h, "Every segment vs the 28.4% baseline",
                          "percentage points \u00b7 right of centre over-indexes for churn"))
_torn = bars("tornado", c, ATTR, "Label", "Attr vs Baseline",
             fill_measure="Attr Bar Color",
             sort_field=mref("Attr vs Baseline"), sort_dir="Descending")
_torn["filterConfig"] = {"filters": [
    topn_filter(ATTR, "Label", "Attr Impact", 10, "fTopImpact")]}
write(d, "tornado", _torn)

six = rects("drivers_six")
for nm, rect, colname, title in [
    ("dContract", six[0], "Contract", "Contract"),
    ("dTenure", six[1], "Tenure Band", "Tenure band"),
    ("dInternet", six[2], "Internet Type", "Internet type"),
    ("dPayment", six[3], "Payment Method", "Payment"),
    ("dSecurity", six[4], "Online Security", "Online security"),
    ("dSupport", six[5], "Premium Tech Support", "Tech support"),
]:
    hh, cc = stack(rect)
    write(d, nm + "H", head_tb(nm + "H", hh, title))
    write(d, nm, bars(nm, cc, FACT, colname, "Churn Rate"))

# ======================================================= PAGE 4
d = add_page("AtRisk", "High-Value at Risk")
write(d, "pageTitle", textbox("pageTitle", HD, [
    ("High-Value at Risk", ts("20pt", INK, "Segoe UI Semibold")),
    ("Two ways to rank a customer, and they disagree - who to call first", ts("10pt", INK2))]))

v = rects("value_two")
h, c = stack(v[0], sub=True)
write(d, "revH", head_tb("revH", h, "Churn rate by LIFETIME revenue quintile",
                         "runs inverse - the cheapest churn most \u00b7 but Q5 still loses $1.51M"))
write(d, "revQ", bars("revQ", c, FACT, "Revenue Quintile", "Churn Rate",
                      sort_field=colref(FACT, "Revenue Quintile"), sort_dir="Ascending"))

h, c = stack(v[1], sub=True)
write(d, "chgH", head_tb("chgH", h, "Churn rate by MONTHLY charge quintile",
                         "runs the other way - premium plans churn most \u00b7 Q5 is $47K/month"))
write(d, "chgQ", bars("chgQ", c, FACT, "Charge Quintile", "Churn Rate", colour=STAYED,
                      sort_field=colref(FACT, "Charge Quintile"), sort_dir="Ascending"))

r = rects("risk_body")
h, c = stack(r[0], sub=True)
write(d, "shortH", head_tb("shortH", h, "Retention shortlist - still with us, high risk",
                           "rule-based score from the page-3 drivers, NOT a predictive model "
                           "(the brief rules ML out of scope)"))
short = table("shortTable", c, [
    proj_c(FACT, "Customer ID", "Customer"),
    proj_c(FACT, "City"),
    proj_c(FACT, "Internet Type", "Internet"),
    proj_c(FACT, "Tenure in Months", "Tenure"),
    proj_m("Avg Monthly Charge", "Monthly $"),
    proj_m("Total Revenue Amt", "Lifetime $"),
    proj_c(FACT, "Risk Score", "Score"),
    proj_m("Risk Pill", "Tier"),
], grid_extra={"imageHeight": lit("20D"), "imageWidth": lit("74D")})
# filterConfig sits at the ROOT of visual.json, as a sibling of "visual" - not inside it
short["filterConfig"] = {"filters": [
    cat_filter("fStayed", "Customer Status", "Stayed"),
    cat_filter("fHighRisk", "Risk Tier", "High"),
    cat_filter("fTopCharge", "Charge Quintile", "Q5 — highest"),
]}
sort_by(short, mref("Avg Monthly Charge"), "Descending")
write(d, "shortTable", short)

h, c = stack(r[1], sub=True)
write(d, "cityH", head_tb("cityH", h, "Churn by city",
                          "zip rolled up to city \u00b7 1,106 cities in the base"))
write(d, "cityTable", sort_by(table("cityTable", c, [
    proj_c(FACT, "City"),
    proj_m("Churned Customers", "Churned"),
    proj_m("Churn Rate", "Rate"),
]), mref("Churned Customers"), "Descending"))

print("pages 2-4 built")
