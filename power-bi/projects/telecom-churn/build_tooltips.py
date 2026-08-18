"""Four report-page tooltips, one per hover context.

Why four and not one: a tooltip only helps if its measures mean something in the context the
reader is hovering. A churn RATE inside a churn-reason row is 100% by construction; inside a
ProfileAttr row the plain [Churn Rate] is blank and only the [Attr *] family resolves. So each
page is built for the context that reaches it, and TOOLTIP_MAP in churnkit.py records which
visual gets which.

Run LAST - apply_tooltips() rewrites visuals that build_p1 / build_p234 have already written.
"""
from churnkit import (CHURNED, INK, INK2, add_tooltip_page, apply_tooltips, textbox, ts,
                      tt_card, tt_grid, tt_title, write)

CELLS, FOOT = tt_grid()


def foot(d, name, text):
    write(d, name, textbox(name, FOOT, [(text, ts("8pt", INK2))], z=300))


def quad(d, rows):
    for nm, rect, meas, label, colour in rows:
        write(d, nm, tt_card(nm, rect, meas, label, colour))


# ---------------------------------------------------------------- rate-based segments
# the six driver small multiples, both quintile tables, churn by city
d = add_tooltip_page("ttSegment", "TT Segment")
write(d, "ttSegTitle", tt_title("ttSegTitle", "TT Segment Label"))
quad(d, [
    ("ttSegN", CELLS[0], "Segment Customers", "Customers in segment", INK),
    ("ttSegR", CELLS[1], "Churn Rate", "Churn rate", CHURNED),
    ("ttSegB", CELLS[2], "Churn Rate vs Baseline", "vs 28.4% baseline (pp)", INK),
    ("ttSegM", CELLS[3], "Monthly Revenue at Risk", "Recurring $ / month", CHURNED),
])
foot(d, "ttSegFoot",
     "Rate is churned ÷ (churned + stayed). Joined customers sit outside both sides.")

# ---------------------------------------------------------------- ProfileAttr segments
# the tornado and both halves of the profile matrix
d = add_tooltip_page("ttAttr", "TT Attribute")
write(d, "ttAttrTitle", tt_title("ttAttrTitle", "Attr Label"))
quad(d, [
    ("ttAttrN", CELLS[0], "Attr Segment Customers", "Customers in segment", INK),
    ("ttAttrR", CELLS[1], "Attr Churn Rate", "Churn rate", CHURNED),
    ("ttAttrB", CELLS[2], "Attr vs Baseline", "vs 28.4% baseline (pp)", INK),
    ("ttAttrD", CELLS[3], "Attr Divergence", "Divergence (pp)", INK),
])
foot(d, "ttAttrFoot",
     "Rate = how often these customers leave. Divergence = whether churners are "
     "concentrated here. They can disagree.")

# ---------------------------------------------------------------- churn reasons
# reason rows are churned-only, so a churn rate here would read 100% on every row
d = add_tooltip_page("ttReason", "TT Reason")
write(d, "ttRsnTitle", tt_title("ttRsnTitle", "TT Segment Label", CHURNED))
quad(d, [
    ("ttRsnN", CELLS[0], "Churned Customers", "Customers who left", CHURNED),
    ("ttRsnS", CELLS[1], "Churned Share of Total", "Share of all churn", CHURNED),
    ("ttRsnM", CELLS[2], "Monthly Revenue at Risk", "Recurring $ / month", CHURNED),
    ("ttRsnA", CELLS[3], "Avg Monthly Charge", "Avg monthly charge", INK),
])
foot(d, "ttRsnFoot",
     "Verbatim reason recorded at churn. Churned customers only — every row here has "
     "already left, so there is no rate to show.")

# ---------------------------------------------------------------- one customer
# its own geometry: the "why" line needs a real strip, not the 24px footer the others use
d = add_tooltip_page("ttCustomer", "TT Customer")
CUS = [{"x": x, "y": y, "width": 144, "height": 56} for y in (48, 112) for x in (8, 168)]
# the longest "why" runs to six rules and wraps to three lines at 8pt, so it gets 56px
# and gives up its caption to get there
WHY = {"x": 8, "y": 176, "width": 304, "height": 56}
write(d, "ttCusTitle", tt_title("ttCusTitle", "TT Customer Label"))
quad(d, [
    ("ttCusT", CUS[0], "Avg Tenure", "Tenure (months)", INK),
    ("ttCusM", CUS[1], "Avg Monthly Charge", "Monthly charge", INK),
    ("ttCusL", CUS[2], "Total Revenue Amt", "Lifetime revenue", INK),
    ("ttCusS", CUS[3], "Customer Risk Score", "Risk score / 100", CHURNED),
])
# the score is a transparent rule set, so the tooltip shows the working, not just the number
write(d, "ttCusWhy", tt_card("ttCusWhy", WHY, "TT Customer Why", "Why this score", INK2,
                             size="8D", show_label=False))

apply_tooltips()
print("tooltips built")
