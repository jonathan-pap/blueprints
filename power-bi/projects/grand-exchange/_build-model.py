"""Hand-off builder — splice the synthetic grand-exchange data into the Power BI SemanticModel.

Reads the CSVs produced by synthetic-data/projects/grand-exchange/generate.py (from the stable
`latest/` folder), infers column types, and writes thick-import TMDL: one table per CSV (each with a
single-line Power Query M partition that loads the CSV), a galaxy-schema relationships.tmdl, a
starter _Measures table, and updates model.tmdl.

Run with Power BI Desktop CLOSED (Desktop re-saves and would clobber the TMDL on next save).

    python _build-model.py
    python _build-model.py --src <folder>   # override CSV source folder

TMDL discipline (see repo memory): only `///` doc comments (never bare `//`); partition source uses
the canonical multi-line `source =` + indented `let`/`in` block (NOT single-line inline let, and NOT
triple-backtick blocks — Desktop mis-parses a single-line inline let as a cyclic reference on load);
UTF-8 no BOM; LF line endings; tabs.
"""
from __future__ import annotations

import argparse
import uuid
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
DEFAULT_SRC = HERE.parent.parent.parent / "synthetic-data" / "outputs" / "grand-exchange" / "latest"
DEST = HERE / "grand-exchange.SemanticModel" / "definition"
TABLES_DIR = DEST / "tables"

# stable lineage tags so re-runs produce clean diffs
_NS = uuid.UUID("9e1c0de5-9a11-4b0e-8b0e-0123456789ab")
def tag(s: str) -> str:
    return str(uuid.uuid5(_NS, s))

# dim tables first (parents), then bridges/facts — also the PBI_QueryOrder
TABLE_ORDER = [
    "DimRarity", "DimRegion", "DimSeller", "DimMonster", "DimDate", "DimMarketEvent",
    "DimItem", "DimRecipe",
    "FactRecipeIngredient", "FactDropTable", "FactItemSource",
    "FactMarketPriceDaily", "FactTrade",
]
DATE_TABLE = "DimDate"
DATE_COLS = {"Date", "StartDate", "EndDate"}

# Galaxy schema. (from_table, from_col, to_table, to_col, active)
# Inactive ones avoid ambiguous paths / are role-playing — activate via USERELATIONSHIP in measures.
RELATIONSHIPS = [
    ("FactMarketPriceDaily", "ItemKey", "DimItem", "ItemKey", True),
    ("FactMarketPriceDaily", "DateKey", "DimDate", "DateKey", True),
    ("FactTrade", "ItemKey", "DimItem", "ItemKey", True),
    ("FactTrade", "DateKey", "DimDate", "DateKey", True),
    ("FactTrade", "SellerKey", "DimSeller", "SellerKey", True),
    ("FactTrade", "BuyerSellerKey", "DimSeller", "SellerKey", False),   # role-playing (buyer)
    ("FactDropTable", "MonsterKey", "DimMonster", "MonsterKey", True),
    ("FactDropTable", "ItemKey", "DimItem", "ItemKey", True),
    ("FactItemSource", "ItemKey", "DimItem", "ItemKey", True),
    ("FactRecipeIngredient", "RecipeKey", "DimRecipe", "RecipeKey", True),
    ("FactRecipeIngredient", "IngredientItemKey", "DimItem", "ItemKey", True),
    ("DimRecipe", "OutputItemKey", "DimItem", "ItemKey", False),        # inactive: avoids 2nd path to DimItem
    ("DimMonster", "RegionKey", "DimRegion", "RegionKey", True),
    ("DimItem", "RarityKey", "DimRarity", "RarityKey", True),
]


def infer(col: str, series: pd.Series):
    """-> (tmdl_dataType, m_type, summarizeBy, formatString|None, is_general_number)"""
    if col in DATE_COLS:
        return "dateTime", "type date", "none", "Long Date", False
    if col.endswith("Key") or col.endswith("Id"):
        return "int64", "Int64.Type", "none", "0", False
    dt = series.dtype
    if pd.api.types.is_bool_dtype(dt):
        return "boolean", "type logical", "none", None, False
    if pd.api.types.is_integer_dtype(dt):
        return "int64", "Int64.Type", "sum", "0", False
    if pd.api.types.is_float_dtype(dt):
        return "double", "type number", "sum", None, True
    return "string", "type text", "none", None, False


def m_partition_lines(csv_path: Path, cols: list[tuple[str, str]]) -> list[str]:
    """Multi-line M block, matching the canonical form Desktop emits (test/financials works this way).
    A single-line inline `let ... in` is parsed differently by Desktop and triggers a spurious
    'cyclic reference' on load — so we use the standard `source =` + indented block form."""
    p = str(csv_path).replace("/", "\\")
    transforms = ", ".join(f'{{"{c}", {mt}}}' for c, mt in cols)
    return [
        "\t\tsource =",
        "\t\t\t\tlet",
        f'\t\t\t\t\tSource = Csv.Document(File.Contents("{p}"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),',
        "\t\t\t\t\tPromoted = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),",
        f"\t\t\t\t\tTyped = Table.TransformColumnTypes(Promoted, {{{transforms}}})",
        "\t\t\t\tin",
        "\t\t\t\t\tTyped",
    ]


def build_table_tmdl(table: str, df: pd.DataFrame, csv_path: Path) -> str:
    L = [f"table {table}", f"\tlineageTag: {tag(table)}"]
    if table == DATE_TABLE:
        L.append("\tdataCategory: Time")
    L.append("")

    m_cols = []
    for col in df.columns:
        data_type, m_type, summ, fmt, general = infer(col, df[col])
        m_cols.append((col, m_type))
        L.append(f"\tcolumn {col}")
        L.append(f"\t\tdataType: {data_type}")
        if fmt:
            L.append(f"\t\tformatString: {fmt}")
        L.append(f"\t\tlineageTag: {tag(table + '.' + col)}")
        L.append(f"\t\tsummarizeBy: {summ}")
        L.append(f"\t\tsourceColumn: {col}")
        L.append("")
        L.append("\t\tannotation SummarizationSetBy = Automatic")
        if general:
            L.append("")
            L.append('\t\tannotation PBI_FormatHint = {"isGeneralNumber":true}')
        L.append("")

    L.append(f"\tpartition {table} = m")
    L.append("\t\tmode: import")
    L.extend(m_partition_lines(csv_path, m_cols))
    L.append("")
    L.append("\tannotation PBI_ResultType = Table")
    L.append("")
    return "\n".join(L)


def build_relationships_tmdl() -> str:
    blocks = []
    for ft, fc, tt, tc, active in RELATIONSHIPS:
        guid = tag(f"rel:{ft}.{fc}->{tt}.{tc}")
        b = [f"relationship {guid}"]
        if not active:
            b.append("\tisActive: false")
        b.append(f"\tfromColumn: {ft}.{fc}")
        b.append(f"\ttoColumn: {tt}.{tc}")
        blocks.append("\n".join(b))
    return "\n\n".join(blocks) + "\n"


def build_measures_tmdl() -> str:
    # starter measures referencing real columns; time-intel uses the marked DimDate
    return '''table _Measures
\tisHidden
\tlineageTag: {tag}

\t/// Total gold value of all trades.
\tmeasure 'Total Trade Value' = SUM(FactTrade[TotalPrice])
\t\tformatString: $#,##0
\t\tdisplayFolder: 1. Headline
\t\tlineageTag: {m1}

\t/// Total units traded across all trades.
\tmeasure 'Trade Quantity' = SUM(FactTrade[Quantity])
\t\tformatString: #,##0
\t\tdisplayFolder: 1. Headline
\t\tlineageTag: {m2}

\t/// Number of trade transactions.
\tmeasure 'Trade Count' = COUNTROWS(FactTrade)
\t\tformatString: #,##0
\t\tdisplayFolder: 1. Headline
\t\tlineageTag: {m3}

\t/// Distinct tradeable items that changed hands.
\tmeasure 'Distinct Items Traded' = DISTINCTCOUNT(FactTrade[ItemKey])
\t\tformatString: #,##0
\t\tdisplayFolder: 1. Headline
\t\tlineageTag: {m4}

\t/// Average daily market price across items in context.
\tmeasure 'Avg Market Price' = AVERAGE(FactMarketPriceDaily[AvgPrice])
\t\tformatString: $#,##0.00
\t\tdisplayFolder: 2. Market
\t\tlineageTag: {m5}

\t/// Total units listed on the market (daily snapshot sum).
\tmeasure 'Total Market Volume' = SUM(FactMarketPriceDaily[Volume])
\t\tformatString: #,##0
\t\tdisplayFolder: 2. Market
\t\tlineageTag: {m6}

\t/// Active listings on the market (daily snapshot sum).
\tmeasure 'Active Listings' = SUM(FactMarketPriceDaily[ListingsCount])
\t\tformatString: #,##0
\t\tdisplayFolder: 2. Market
\t\tlineageTag: {m7}

\t/// Trade value year-to-date (needs the marked DimDate date table).
\tmeasure 'Trade Value YTD' =
\t\t\tCALCULATE(
\t\t\t\t[Total Trade Value],
\t\t\t\tDATESYTD(DimDate[Date])
\t\t\t)
\t\tformatString: $#,##0
\t\tdisplayFolder: 3. Time Intelligence
\t\tlineageTag: {m8}

\t/// Trade value in the same period one year ago.
\tmeasure 'Trade Value PY' =
\t\t\tCALCULATE(
\t\t\t\t[Total Trade Value],
\t\t\t\tSAMEPERIODLASTYEAR(DimDate[Date])
\t\t\t)
\t\tformatString: $#,##0
\t\tdisplayFolder: 3. Time Intelligence
\t\tlineageTag: {m9}

\tcolumn _
\t\tlineageTag: {mc}
\t\tisNameInferred
\t\tsourceColumn: [_]

\tpartition _Measures = calculated
\t\tmode: import
\t\tsource = ROW("_", "")

\tannotation PBI_ResultType = Table
'''.format(
        tag=tag("_Measures"),
        m1=tag("_Measures.Total Trade Value"), m2=tag("_Measures.Trade Quantity"),
        m3=tag("_Measures.Trade Count"), m4=tag("_Measures.Distinct Items Traded"),
        m5=tag("_Measures.Avg Market Price"), m6=tag("_Measures.Total Market Volume"),
        m7=tag("_Measures.Active Listings"), m8=tag("_Measures.Trade Value YTD"),
        m9=tag("_Measures.Trade Value PY"), mc=tag("_Measures._"),
    )


def update_model_tmdl(all_tables: list[str]):
    path = DEST / "model.tmdl"
    text = path.read_text(encoding="utf-8")
    # drop any prior ref table / PBI_QueryOrder so re-runs are idempotent
    lines = [ln for ln in text.splitlines()
             if not ln.startswith("ref table ")
             and not ln.startswith("annotation PBI_QueryOrder")]
    text = "\n".join(lines)
    order = ", ".join(f'"{t}"' for t in all_tables)
    query_order = f'annotation PBI_QueryOrder = [{order}]'
    ref_block = "\n".join(f"ref table {t}" for t in all_tables)
    # insert PBI_QueryOrder after PBI_ProTooling; ref tables before ref cultureInfo
    if "annotation PBI_ProTooling" in text:
        text = text.replace("annotation PBI_ProTooling = [\"DevMode\"]",
                            "annotation PBI_ProTooling = [\"DevMode\"]\n\n" + query_order, 1)
    text = text.replace("ref cultureInfo en-US", ref_block + "\n\nref cultureInfo en-US", 1)
    path.write_text(text.rstrip("\n") + "\n", encoding="utf-8", newline="\n")


def write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip("\n") + "\n", encoding="utf-8", newline="\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=str(DEFAULT_SRC))
    args = ap.parse_args()
    src = Path(args.src)

    print(f"[handoff] source CSVs : {src}")
    print(f"[handoff] dest model  : {DEST}\n")
    if not src.exists():
        raise SystemExit(f"source folder not found: {src}  (run generate.py first)")

    all_tables = TABLE_ORDER + ["_Measures"]
    for t in TABLE_ORDER:
        csv = src / f"{t}.csv"
        if not csv.exists():
            raise SystemExit(f"missing CSV: {csv}")
        df = pd.read_csv(csv)
        write(TABLES_DIR / f"{t}.tmdl", build_table_tmdl(t, df, csv))
        flags = " [date table]" if t == DATE_TABLE else ""
        print(f"  [ok] tables/{t}.tmdl  ({len(df.columns)} cols, {len(df):,} rows){flags}")

    write(TABLES_DIR / "_Measures.tmdl", build_measures_tmdl())
    print("  [ok] tables/_Measures.tmdl  (9 measures)")

    write(DEST / "relationships.tmdl", build_relationships_tmdl())
    inactive = sum(1 for *_, a in RELATIONSHIPS if not a)
    print(f"  [ok] relationships.tmdl  ({len(RELATIONSHIPS)} rels, {inactive} inactive)")

    update_model_tmdl(all_tables)
    print(f"  [ok] model.tmdl  (ref {len(all_tables)} tables + PBI_QueryOrder)")

    print("\n[done] hand-off spliced. Open grand-exchange.pbip in Desktop and Refresh to load data.")
    print("       (Desktop must have been CLOSED during this splice.)")


if __name__ == "__main__":
    main()
