"""Add a dynamic format string to every count/volume measure (those with
formatString: #,0). Rule:
  |v| < 1,000,000      -> "#,0"        full number (e.g. 12,577)
  |v| < 1,000,000,000  -> "#,0.0,,\\M"  millions   (e.g. 12.6M)
  else                 -> "#,0.0,,,\\B" billions   (e.g. 1.2B)
Percent measures (formatString: 0.0%) are left untouched.
"""
p = "gddt.SemanticModel/definition/tables/_Measures.tmdl"
with open(p, encoding="utf-8") as f:
    lines = f.readlines()

# Single-line dynamic format definition (avoid triple-backtick multi-line blocks).
FSD = (
    '\t\tformatStringDefinition = '
    'SWITCH ( TRUE (), '
    'ABS ( SELECTEDMEASURE () ) < 1000000, "#,0", '
    'ABS ( SELECTEDMEASURE () ) < 1000000000, "#,0.0,,\\M", '
    '"#,0.0,,,\\B" )\n'
)

out, count = [], 0
for line in lines:
    out.append(line)
    if line.rstrip("\n") == "\t\tformatString: #,0":
        out.append(FSD)
        count += 1

with open(p, "w", encoding="utf-8", newline="\n") as f:
    f.writelines(out)
print(f"added formatStringDefinition to {count} measures")
