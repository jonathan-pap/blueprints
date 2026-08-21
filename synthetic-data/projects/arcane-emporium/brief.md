# Brief — Arcane Emporium

**Contoso, reskinned as fantasy retail.** A chain of 8 enchanted-goods shops across three realms
(Eldoria / Grimmwald / Sunspire) selling potions, scrolls, enchanted weapons, artifacts and reagents to
20 named customers (adventurers, collectors, guilds, nobles). Four years of daily Gold sales
(2023–2026, ~100K rows), +12% YoY, Frostfall festival peak (Nov/Dec); flagship items and big-spender
customers pareto-led inside exactly-pinned category and customer-type shares.

- **Purpose:** demo star for Power BI — pretty names, coherent numbers that tie out at every grain.
- **Config:** [`config.yaml`](config.yaml) (the declaration IS the schema) · seed 1337.
- **Run:** `python 03-generate/generate.py projects/arcane-emporium/config.yaml` →
  `python 05-review/reconcile.py projects/arcane-emporium/config.yaml`
- **Output:** `outputs/arcane-emporium/latest/` — DimDate, DimShop, DimItem, DimCustomer, FactSales (~100K rows).
