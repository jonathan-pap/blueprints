# Brief — Arcane Emporium

**Contoso, reskinned as fantasy retail.** A chain of 8 enchanted-goods shops across three realms
(Eldoria / Grimmwald / Sunspire) selling potions, scrolls, enchanted weapons, artifacts and reagents.
Two years of daily Gold sales (2024–2025), +12% YoY, Frostfall festival peak (Nov/Dec), flagship items
pareto-led inside exactly-pinned category shares.

- **Purpose:** demo star for Power BI — pretty names, coherent numbers that tie out at every grain.
- **Config:** [`config.yaml`](config.yaml) (the declaration IS the schema) · seed 1337.
- **Run:** `python 03-generate/generate.py projects/arcane-emporium/config.yaml` →
  `python 05-review/reconcile.py projects/arcane-emporium/config.yaml`
- **Output:** `outputs/arcane-emporium/latest/` — DimDate, DimShop, DimItem, FactSales (~77K rows).
