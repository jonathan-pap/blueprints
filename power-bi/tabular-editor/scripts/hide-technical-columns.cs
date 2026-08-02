// hide-technical-columns.cs — hide key/technical columns and stop numeric keys aggregating.
// Runs in Tabular Editor 2 and 3. See ../compatibility.md.
// Whole-model. Heuristic: names ending Key/Id/ID or starting '_'. Tune to your conventions.

int hidden = 0;
int fixedAgg = 0;

foreach (var c in Model.AllColumns)
{
    var name = c.Name;
    bool isKey = name.EndsWith("Key") || name.EndsWith("Id") || name.EndsWith("ID") || name.StartsWith("_");
    if (!isKey) continue;

    if (!c.IsHidden)
    {
        c.IsHidden = true;
        hidden++;
    }

    // A numeric key that sums by default is a classic footgun — set it to not summarise.
    if ((c.DataType == DataType.Int64 || c.DataType == DataType.Decimal || c.DataType == DataType.Double)
        && c.SummarizeBy != AggregateFunction.None)
    {
        c.SummarizeBy = AggregateFunction.None;
        fixedAgg++;
    }
}

Output("hide-technical-columns: hid " + hidden + " columns; set SummarizeBy=None on " + fixedAgg + ". Save to persist.");
