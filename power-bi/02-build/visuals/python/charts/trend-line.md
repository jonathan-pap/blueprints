# Python — trend line

A trend line drawn by a Python script visual — for a fitted or smoothed trend the native line chart can't produce. Script visuals render as a static image: they receive filters but can't cross-filter back, and they need Python installed wherever the report is rendered.

## Bindings

```bash
pbir visuals bind "<...>/MyPyTrend.Visual" \
  -a "Values:Date.Month"     -t Column \
  -a "Values:Sales.Revenue"  -t Measure
```

## Script

```python
import matplotlib.pyplot as plt
import pandas as pd

dataset["Month"] = pd.to_datetime(dataset["Month"])
data = dataset.sort_values("Month")

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(data["Month"], data["Revenue"], color="#118DFF", linewidth=2, marker="o")
ax.set_ylabel("Revenue")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.show()
```

## Sort by date

Power BI doesn't guarantee row order. Sort the DataFrame before plotting.

## Convert dates

If `Date.Month` is bound as a column (not a date), it may come through as string. `pd.to_datetime` is defensive.

## Reference

- `../examples/script/trend-line.py`
- `../examples/visual/trend-line.json`
