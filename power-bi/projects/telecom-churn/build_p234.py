"""Pages 2-4: Customer Profile, Churn Drivers, High-Value at Risk."""
from churnkit import (CHURNED, FACT, INK, INK2, JOINED, RULE, STAYED, SURFACE, add_page,
                      head_tb, in_filter, lit, measure, page_chrome, proj_c, proj_m, rects,
                      solid, stack, textbox, ts, vis, write)

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


def table(name, rect, projections, grid_extra=None, z=200, values_extra=None):
    g = dict(GRID)
    if grid_extra:
        g.update(grid_extra)
    vals = VALS
    if values_extra:
        p = dict(VALS[0]["properties"])
        p.update(values_extra)
        vals = [{"properties": p}]
    return vis(name, "tableEx", rect, z,
               query={"Values": {"projections": projections}},
               objects={"grid": [{"properties": g}], "columnHeaders": HDRS,
                        "values": vals, "total": NOTOT})


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



# ======================================================= PAGE 2
d = add_page("Profile", "Customer Profile")
page_chrome(d, "Customer Profile",
            "Churned vs Stayed vs Joined - where the three groups actually differ \u00b7 "
            "read the matrices ACROSS a row, never down a column")

s = rects("profile_summary")[0]
n = rects("profile_note")[0]
h, c = stack(s)
write(d, "sumH", head_tb("sumH", h, "The three groups at a glance"))
write(d, "sumTable", sort_by(table("sumTable", c, [
    proj_c(FACT, "Customer Status", "Status"),
    proj_m("Total Customers", "Customers"),
    proj_m("Avg Tenure", "Avg tenure (mo)"),
    proj_m("Avg Monthly Charge", "Avg monthly $"),
    proj_m("Pct Month to Month", "On month-to-month"),
]), mref("Total Customers"), "Descending"))

# the numbers above say WHAT differs; this says what it MEANS. Colour-coded to the
# legend so the three lines bind to the three rows without repeating the labels.
nh, nc = stack(n)
write(d, "noteH", head_tb("noteH", nh, "Who these people are"))
write(d, "noteTb", textbox("noteTb", nc, [
    ("Churned - short-tenure fiber customers on month-to-month at premium rates, "
     "mostly without security or support add-ons.", ts("10pt", CHURNED)),
    ("Stayed - long-tenure and contracted; two thirds sit on a one- or two-year term.",
     ts("10pt", STAYED)),
    ("Joined - arrived this quarter on light month-to-month plans. Every one of them is "
     "in the 0-6 month band by definition, so tenure tells you nothing about them yet.",
     ts("10pt", JOINED)),
]))

# The matrix is 29 rows. As ONE full-width table it rendered 13 and scrolled the other 16
# out of sight - the widest visual on the page was also the one hiding the most data. Split
# in two it reads side by side with nothing below the fold, and each half stays wide enough
# for the in-cell dumbbell.
b = rects("profile_body_2")
HALVES = [
    ("A", b[0], ["Contract", "Tenure", "Internet", "Payment"],
     "Profile comparison - teal dot = stayers, magenta = churners"),
    ("B", b[1], ["Offer", "Monthly $", "Online security", "Tech support"],
     "Profile comparison, continued - divergence is churned minus stayed, in pp"),
]
for tag, rect, attrs, htitle in HALVES:
    h, c = stack(rect)
    write(d, "divH" + tag, head_tb("divH" + tag, h, htitle))
    t = sort_by(table("divTable" + tag, c, [
        proj_c(ATTR, "Attribute"),
        proj_c(ATTR, "Value"),
        proj_m("Attr Churn Share", "Churn"),
        proj_m("Attr Stay Share", "Stay"),
        proj_m("Attr Join Share", "Join"),
        proj_m("Attr Dumbbell", "stay - churn"),
        proj_m("Attr Divergence", "Diverg."),
    ], grid_extra={"imageHeight": lit("14D"), "imageWidth": lit("140D"),
                   "rowPadding": lit("0D")},
        values_extra={"fontSize": lit("9D")}),
        colref(ATTR, "SortKey"), "Ascending")
    # filterConfig is a sibling of "visual", at the ROOT of visual.json - nesting it
    # inside "visual" is a SCHEMA_ERROR
    t["filterConfig"] = {"filters": [
        in_filter(ATTR, "Attribute", attrs, "fAttrHalf" + tag)]}
    write(d, "divTable" + tag, t)

# ======================================================= PAGE 3
d = add_page("Drivers", "Churn Drivers")
page_chrome(d, "Churn Drivers",
            "Churn RATE by segment, ranked against the 28.4% baseline - rate not count, "
            "because a big segment churns more simply by being big")

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
# keep is the value whitelist. Online Security / Premium Tech Support are an empty string
# - not BLANK - for the 1,526 customers with no internet, so an unfiltered bar chart drew a
# nameless bar at 8.4% next to Yes and No. The add-on simply does not apply to them, so they
# are excluded here; Internet uses the labelled [Internet] column so its None cohort stays.
for nm, rect, colname, title, keep in [
    ("dContract", six[0], "Contract", "Contract", None),
    ("dTenure", six[1], "Tenure Band", "Tenure band", None),
    ("dInternet", six[2], "Internet", "Internet type", None),
    ("dPayment", six[3], "Payment Method", "Payment", None),
    ("dSecurity", six[4], "Online Security", "Online security", ["Yes", "No"]),
    ("dSupport", six[5], "Premium Tech Support", "Tech support", ["Yes", "No"]),
]:
    hh, cc = stack(rect)
    write(d, nm + "H", head_tb(nm + "H", hh, title))
    v = bars(nm, cc, FACT, colname, "Churn Rate")
    if keep:
        v["filterConfig"] = {"filters": [in_filter(FACT, colname, keep, "f" + nm)]}
    write(d, nm, v)

# ======================================================= PAGE 4
d = add_page("AtRisk", "High-Value at Risk")
page_chrome(d, "High-Value at Risk",
            "Two ways to rank a customer, and they disagree - who to call first")

# A plain bar chart could show the RATE but not the money beside it, and the money is the
# whole argument of this page - Q5 churns least and still loses the most. So each panel is a
# table: quintile, SVG track bar, rate, money. Sorted Q5 first: the reader wants the most
# valuable customers at the top, not the cheapest.
v = rects("value_two")
for tag, rect, qcol, money, mlabel, title, sub, foot in [
    ("rev", v[0], "Revenue Quintile", "Churned Revenue", "Lifetime lost",
     "Churn rate by LIFETIME revenue quintile",
     "Total Revenue quintiles \u00b7 revenue already lost at right",
     "Lifetime value and churn run inversely - long tenure both builds revenue and predicts "
     "staying. The top quintile still carries the largest absolute loss, $1.44M."),
    ("chg", v[1], "Charge Quintile", "Monthly Revenue at Risk", "Monthly lost",
     "Churn rate by MONTHLY charge quintile",
     "Monthly Charge quintiles \u00b7 recurring revenue lost at right",
     "Recurring charge ranks the opposite way. The peak is Q4 at 36.9%, not Q5 - the very "
     "highest bills skew to long-tenure fibre contracts. Q4 and Q5 together lose $86K a month "
     "of the $137.1K total."),
]:
    h, c = stack(rect, sub=True)
    write(d, tag + "H", head_tb(tag + "H", h, title, sub))
    # table above, footnote below, filling the 224px body as 176 + 8 + 40. Both halves were
    # sized against the RENDERED row height, not guessed: at rowPadding 4 / 10pt a row is
    # ~35px and five of them plus a header overflow 176, so the table drew a scroll track
    # with nothing to scroll to. At rowPadding 1 / 9pt a row is ~26px and it fits with slack,
    # which leaves the footnote the 40px it needs for two lines.
    tbl = dict(c, height=176)
    note = {"x": c["x"], "y": c["y"] + 184, "width": c["width"], "height": 40}
    write(d, tag + "Q", sort_by(table(tag + "Q", tbl, [
        proj_c(FACT, qcol, "Quintile"),
        proj_m("Quintile Bar", "vs the 28.4% baseline"),
        proj_m("Churn Rate", "Churn rate"),
        proj_m(money, mlabel),
    ], grid_extra={"imageHeight": lit("16D"), "imageWidth": lit("200D"),
                   "rowPadding": lit("1D")},
        values_extra={"fontSize": lit("9D")}),
        colref(FACT, qcol), "Descending"))
    write(d, tag + "Foot", textbox(tag + "Foot", note, [(foot, ts("9pt", INK2))]))

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
    proj_m("Risk Signal", "Tier"),
], grid_extra={"imageHeight": lit("20D"), "imageWidth": lit("96D")})
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
