# Brief — Guild Provisioners

**Northwind, reskinned as a fantasy wholesale guild.** A provisioning guild supplying 15 patrons
(taverns, adventuring guilds, academies, noble courts) with 20 wares (provisions / armaments /
alchemical / textiles) from named suppliers. Two years of daily Gold orders, +6% YoY, campaign-season
peak, ware pareto inside exactly-pinned ware-type shares; supplier mix emerges from the ware ranking.

- **Purpose:** demo star for Power BI — the classic orders-shape dataset with fantasy flavor.
- **Config:** [`config.yaml`](config.yaml) · seed 2024.
- **Run:** `python 03-generate/generate.py projects/guild-provisioners/config.yaml` →
  `python 05-review/reconcile.py projects/guild-provisioners/config.yaml`
- **Output:** `outputs/guild-provisioners/latest/` — DimDate, DimPatron, DimWare, FactOrders (~33K rows).
