# Python — KPI card

A big number with a small trend below. Use Python KPI when matplotlib gives you the typography or layered annotation control you want.

For interactive KPI use Deneb (`../../deneb/charts/kpi-card.md`). For inline KPI inside a table use SVG.

## Bindings

```bash
pbir visuals bind "<...>/MyPyKpi.Visual" \
  -a "Values:Sales.Revenue"       -t Measure \
  -a "Values:Sales.Revenue 1YP"   -t Measure \
  -a "Values:Date.Month"          -t Column \
  -a "Values:Sales.Revenue MoM"   -t Measure
```

## Script

See `../../examples/script/kpi-card.py` for the full pattern; outline:

```python
import matplotlib.pyplot as plt

actual = dataset["Revenue"].iloc[-1]            # or sum, depending on bind
target = dataset["Revenue 1YP"].iloc[-1]
delta  = actual - target
pct    = delta / target

fig = plt.figure(figsize=(4, 2.5))
fig.text(0.05, 0.55, f"{actual/1e6:.1f}M",
         fontsize=36, fontweight="bold", color="#252423")
fig.text(0.05, 0.30, f"{pct:+.1%} vs target",
         fontsize=12, color="#2B7A78" if pct >= 0 else "#D4602E")
# small trend axes below
ax = fig.add_axes([0.05, 0.05, 0.9, 0.18])
ax.plot(dataset["Month"], dataset["Revenue"], color="#118DFF")
ax.axis("off")
plt.show()
```

## Why this is hard

Python visuals don't have native title slots; everything is figure text. Layout requires explicit coords.

## Reference

- `../../examples/visual/kpi-card.json` — full PBIR visual
