// fix-measure-variables.cs — rename measure DAX VARs to start with '_' (declaration + references).
// Runs in Tabular Editor 2 and 3. See ../compatibility.md.  Pairs with check-measure-variables.cs
// and the MEASURE_VAR_UNDERSCORE_PREFIX BPA rule.
//
// DRY-RUN by default. Review the list, then set  apply = true  and re-run to write, then SAVE.
// Renames each offending VAR name 'x' -> '_x' only where it appears as a BARE identifier in CODE —
// it skips string literals "..." (incl. "" escapes), // and /* */ comments, [columns], and 'tables'.
// CAVEAT: matching is case-sensitive; if a variable shares a name with something referenced bare,
// the dry-run will show it — check before applying.

bool apply = false;                    // <-- set true to actually rename

// blank out strings + comments so VAR-name DETECTION never trips on text inside them
Func<string, string> codeOnly = s =>
{
    s = System.Text.RegularExpressions.Regex.Replace(s, "\"(?:[^\"]|\"\")*\"", " ");  // "strings"
    s = System.Text.RegularExpressions.Regex.Replace(s, "//[^\r\n]*", " ");           // // line comments
    s = System.Text.RegularExpressions.Regex.Replace(s, "/\\*[\\s\\S]*?\\*/", " ");   // /* block comments */
    return s;
};

var declRx = new System.Text.RegularExpressions.Regex(@"(?i)\bVAR\s+([A-Za-z][A-Za-z0-9_]*)");

var targets = Selected.Measures.Any()
    ? Selected.Measures
    : (IEnumerable<Measure>)Model.AllMeasures;

int changed = 0;
var sb = new System.Text.StringBuilder();

foreach (var m in targets)
{
    var expr = m.Expression ?? "";

    // declared VAR names not starting with '_' (found in code only, not strings/comments)
    var names = new System.Collections.Generic.HashSet<string>();
    foreach (System.Text.RegularExpressions.Match mt in declRx.Matches(codeOnly(expr)))
    {
        var n = mt.Groups[1].Value;
        if (!n.StartsWith("_")) names.Add(n);
    }
    if (names.Count == 0) continue;

    var newExpr = expr;
    foreach (var n in names)
    {
        var esc = System.Text.RegularExpressions.Regex.Escape(n);
        // Alternation: a string literal OR a comment OR the bare identifier. Strings/comments are
        // matched first and returned unchanged, so 'n' inside them is never renamed.
        var pat = "\"(?:[^\"]|\"\")*\""                       // "string"
                + "|//[^\r\n]*"                               // line comment
                + "|/\\*[\\s\\S]*?\\*/"                       // block comment
                + "|(?<![A-Za-z0-9_'\\[])" + esc + "(?![A-Za-z0-9_])";  // the identifier token

        newExpr = System.Text.RegularExpressions.Regex.Replace(newExpr, pat,
            mm => mm.Value == n ? "_" + n : mm.Value);       // only the identifier match equals n
    }

    if (newExpr != expr)
    {
        changed++;
        sb.AppendLine("• " + m.DaxObjectFullName + "  ->  " + string.Join(", ", names));
        if (apply) m.Expression = newExpr;
    }
}

Output(
    (apply ? "APPLIED — renamed vars in " : "DRY-RUN — would rename vars in ")
    + changed + " measure(s)"
    + (apply ? ". SAVE to persist:\n\n" : ". Set apply=true to write:\n\n")
    + sb.ToString());
