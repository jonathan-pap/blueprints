#!/usr/bin/env python3
"""
Hand off a generated star (from 03-generate/generate.py) into a Power BI PBIP model - TMDL splice.

Writes into <target>/<name>.SemanticModel/definition/:
  expressions.tmdl          SourceFolder parameter -> the job's outputs/<job>/latest/ folder
  tables/<Table>.tmdl       one typed import table per CSV (M partition reads SourceFolder & "<Table>.csv")
  tables/_Measures.tmdl     measure home seeded with Total <measure> / row count / averages
  relationships.tmdl        fact -> dim on the <Dim>Key columns
  model.tmdl                `ref table` lines appended (idempotent)

Power BI Desktop must be CLOSED on the target (Desktop re-saves and would clobber the splice).
On first open, refresh (Home > Refresh, or via the Modeling MCP) to load the CSVs.

Usage:
    python handoff_to_pbi.py <config.yaml> --target <path-to-pbi-project-folder>
"""
import sys, os, re, argparse, uuid
import pandas as pd, yaml

TAB = "\t"
DATE_SORT = {"MonthName": "Month", "DayName": "DayNum", "MonthYear": "YearMonth"}
DATE_HIDDEN = {"Month", "DayNum", "YearMonth", "DateKey"}


def tag():
    return str(uuid.uuid4())


def quote(name):
    return "'" + name + "'" if re.search(r"[^A-Za-z0-9_]", name) else name


def col_block(name, dtype, hidden=False, key=False, summarize="none", fmt=None, sort_by=None, unique=False):
    out = [TAB + "column " + quote(name), TAB * 2 + "dataType: " + dtype]
    if unique:
        out.append(TAB * 2 + "isUnique")
    if hidden:
        out.append(TAB * 2 + "isHidden")
    if key:
        out.append(TAB * 2 + "isKey")
    if fmt:
        out.append(TAB * 2 + "formatString: " + fmt)
    out.append(TAB * 2 + "lineageTag: " + tag())
    out.append(TAB * 2 + "summarizeBy: " + summarize)
    out.append(TAB * 2 + "sourceColumn: " + name)
    if sort_by:
        out.append(TAB * 2 + "sortByColumn: " + sort_by)
    return "\n".join(out) + "\n"


def m_type(dtype, is_date):
    if is_date:
        return "type date"
    return {"int64": "Int64.Type", "double": "type number"}.get(dtype, "type text")


def partition_block(table, types, rounding):
    typed = ", ".join('{"%s", %s}' % (c, t) for c, t in types)
    ind = TAB * 4
    lines = [
        TAB + "partition " + table + " = m",
        TAB * 2 + "mode: import",
        TAB * 2 + "source =",
        ind + "let",
        ind + '    Source = Csv.Document(File.Contents(SourceFolder & "' + table + '.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),',
        ind + "    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),",
        ind + "    Typed = Table.TransformColumnTypes(Promoted, {" + typed + "})" + ("," if rounding else ""),
    ]
    if rounding:
        r = ", ".join('{"%s", each Number.Round(_, 2), type number}' % c for c in rounding)
        lines.append(ind + "    Rounded = Table.TransformColumns(Typed, {" + r + "})")
        lines += [ind + "in", ind + "    Rounded"]
    else:
        lines += [ind + "in", ind + "    Typed"]
    return "\n".join(lines) + "\n"


def pandas_dtype(s):
    if pd.api.types.is_integer_dtype(s):
        return "int64"
    if pd.api.types.is_float_dtype(s):
        return "double"
    return "string"


def write(path, text):
    with open(path, "w", encoding="utf-8", newline="\r\n") as fh:
        fh.write(text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("config")
    ap.add_argument("--target", required=True)
    a = ap.parse_args()
    cfg = yaml.safe_load(open(a.config, encoding="utf-8"))
    job = cfg.get("name", "job")
    outdir = os.path.abspath(cfg.get("output", {}).get("dir") or "outputs/%s/latest" % job)
    src_folder = outdir.replace("\\", "/").rstrip("/") + "/"

    target = os.path.abspath(a.target)
    pbip = [f for f in os.listdir(target) if f.endswith(".pbip")]
    if not pbip:
        sys.exit("no .pbip in " + target)
    name = pbip[0][:-5]
    defdir = os.path.join(target, name + ".SemanticModel", "definition")
    tdir = os.path.join(defdir, "tables")
    os.makedirs(tdir, exist_ok=True)

    dims = cfg["dimensions"]
    facts = cfg["facts"]
    dim_key = {d: ("DateKey" if s.get("type") == "calendar" else s.get("key", d + "Key")) for d, s in dims.items()}
    fk_cols = set(dim_key.values())
    tables, measures, rels = [], [], []

    # ---- dimension tables ----
    for d, spec in dims.items():
        tname = "Dim" + d
        df = pd.read_csv(os.path.join(outdir, tname + ".csv"), nrows=5000)
        is_cal = spec.get("type") == "calendar"
        cols, types = [], []
        for c in df.columns:
            dt = pandas_dtype(df[c])
            is_date = is_cal and c == "Date"
            if is_date:
                cols.append(col_block(c, "dateTime", unique=True, fmt="dd mmm yyyy"))
            elif c == dim_key[d]:
                cols.append(col_block(c, "int64", hidden=True, key=True))
            elif is_cal:
                hidden = c in DATE_HIDDEN
                cols.append(col_block(c, dt, hidden=hidden, fmt=("0" if dt == "int64" and not hidden else None), sort_by=DATE_SORT.get(c)))
            else:
                cols.append(col_block(c, dt, fmt=("0" if dt == "int64" else None)))
            types.append((c, m_type(dt, is_date)))
        head = "table " + tname + "\n" + TAB + "lineageTag: " + tag() + "\n" + (TAB + "dataCategory: Time\n" if is_cal else "")
        write(os.path.join(tdir, tname + ".tmdl"), head + "\n" + "\n".join(cols) + "\n" + partition_block(tname, types, []))
        tables.append(tname)

    # ---- fact tables (+ measures, relationships) ----
    for f, spec in facts.items():
        tname = "Fact" + f
        df = pd.read_csv(os.path.join(outdir, tname + ".csv"), nrows=5000)
        cols, types, rounding, mcols = [], [], [], []
        for c in df.columns:
            dt = pandas_dtype(df[c])
            if c == f + "Key":
                cols.append(col_block(c, "int64", hidden=True, key=True))
            elif c in fk_cols:
                cols.append(col_block(c, "int64", hidden=True))
            else:  # raw measure column: hidden + summed; explicit measures drive the visuals
                cols.append(col_block(c, dt, hidden=True, summarize="sum", fmt="#,##0"))
                if dt == "double":
                    rounding.append(c)
                mcols.append(c)
                measures.append(("Total " + c, "SUM ( %s[%s] )" % (tname, c), "#,##0"))
            types.append((c, m_type(dt, False)))
        measures.append((f, "COUNTROWS ( %s )" % tname, "#,##0"))
        for c in mcols:
            measures.append(("Avg " + c, "DIVIDE ( [Total %s], [%s] )" % (c, f), "#,##0.0"))
        body = "table " + tname + "\n" + TAB + "lineageTag: " + tag() + "\n\n" + "\n".join(cols) + "\n" + partition_block(tname, types, rounding)
        write(os.path.join(tdir, tname + ".tmdl"), body)
        tables.append(tname)
        for d in spec["grain"]:
            k = dim_key[d]
            rels.append("relationship %s_Dim%s\n%sfromColumn: %s.%s\n%stoColumn: Dim%s.%s\n" % (tname, d, TAB, tname, k, TAB, d, k))

    # ---- _Measures ----
    ml = ["/// Measure home - a one-row calculated table so every measure lives in one place.",
          "table _Measures", TAB + "lineageTag: " + tag(), ""]
    for n, expr, fmt in measures:
        ml += [TAB + "measure " + quote(n) + " = " + expr, TAB * 2 + "formatString: " + fmt,
               TAB * 2 + "displayFolder: Core", TAB * 2 + "lineageTag: " + tag(), ""]
    ml += [TAB + "partition _Measures = calculated", TAB * 2 + "mode: import", TAB * 2 + 'source = ROW ( "_", "" )', ""]
    write(os.path.join(tdir, "_Measures.tmdl"), "\n".join(ml))
    tables.append("_Measures")

    # ---- expressions, relationships, model refs ----
    write(os.path.join(defdir, "expressions.tmdl"),
          "/// Folder holding the generated " + job + " CSVs. Repoint here if the synthetic-data job is re-run elsewhere.\n"
          + 'expression SourceFolder = "' + src_folder + '" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]\n'
          + TAB + "lineageTag: " + tag() + "\n")
    write(os.path.join(defdir, "relationships.tmdl"), "\n".join(rels))
    mpath = os.path.join(defdir, "model.tmdl")
    model = open(mpath, encoding="utf-8").read()
    refs = "".join("ref table %s\n" % t for t in tables if ("ref table %s\n" % t) not in model)
    if refs:
        if "ref cultureInfo" in model:
            model = model.replace("ref cultureInfo", refs + "\nref cultureInfo", 1)
        else:
            model = model.rstrip("\n") + "\n\n" + refs
        with open(mpath, "w", encoding="utf-8", newline="") as fh:
            fh.write(model)

    print("[ok] spliced %d tables + %d relationships into %s" % (len(tables), len(rels), defdir))
    print("     SourceFolder = " + src_folder)
    print("     measures: " + ", ".join(n for n, _, _ in measures))
    print("     open in Desktop and Refresh to load the CSVs (Desktop must have been CLOSED during the splice).")


if __name__ == "__main__":
    main()
