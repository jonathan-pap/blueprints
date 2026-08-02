// create-time-intelligence.cs — generate PY, YTD and YoY% for each base measure.
// Runs in Tabular Editor 2 and 3. See ../compatibility.md.
// Target: selected base measures in the UI; whole model when headless.
// PREREQ: a Date table marked as a date table. Set the date column below.

string dateColumn = "'Date'[Date]";        // <-- your date column, DAX form
string folder     = "Time Intelligence";

var bases = Selected.Measures.Any()
    ? Selected.Measures
    : (IEnumerable<Measure>)Model.AllMeasures;

int created = 0;

foreach (var b in bases)
{
    // skip measures we clearly shouldn't wrap
    if (b.DisplayFolder == folder) continue;

    var t   = b.Table;
    var src = b.DaxObjectName;               // [Base Measure]

    if (t.Measures.Any(x => x.Name == b.Name + " PY") == false)
    {
        var py = t.AddMeasure(b.Name + " PY",
            "CALCULATE ( " + src + ", DATEADD ( " + dateColumn + ", -1, YEAR ) )", folder);
        py.FormatString = b.FormatString;
        created++;
    }

    if (t.Measures.Any(x => x.Name == b.Name + " YTD") == false)
    {
        var ytd = t.AddMeasure(b.Name + " YTD",
            "TOTALYTD ( " + src + ", " + dateColumn + " )", folder);
        ytd.FormatString = b.FormatString;
        created++;
    }

    if (t.Measures.Any(x => x.Name == b.Name + " YoY %") == false)
    {
        var yoy = t.AddMeasure(b.Name + " YoY %",
            "DIVIDE ( " + src + " - [" + b.Name + " PY], [" + b.Name + " PY] )", folder);
        yoy.FormatString = "0.0%;-0.0%;0.0%";
        created++;
    }
}

Output("create-time-intelligence: created " + created + " measures in '" + folder + "'. Save to persist.");
