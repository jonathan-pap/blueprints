# Python — YTD line

Two lines (CY YTD vs PY YTD) on the same axis.

## Bindings

```bash
pbir visuals bind "<...>/MyYtd.Visual" \
  -a "Values:Date.Calendar Month (ie Jan)" -t Column \
  -a "Values:Sales.Revenue YTD"             -t Measure \
  -a "Values:Sales.Revenue YTD PY"          -t Measure
```

## Script

```python
import matplotlib.pyplot as plt

data = dataset.sort_values("Calendar Month (ie Jan)")

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(data["Calendar Month (ie Jan)"], data["Revenue YTD"],
        color="#118DFF", linewidth=2, label="CY")
ax.plot(data["Calendar Month (ie Jan)"], data["Revenue YTD PY"],
        color="#CCCCCC", linewidth=2, linestyle="--", label="PY")
ax.legend(loc="upper left", frameon=False)
ax.set_ylabel("Revenue")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
plt.show()
```

## Sort by ordinal, not alpha

Months sort alphabetically by default ("Apr, Aug, Dec, Feb..."). Either:

- Pre-sort by a hidden month-number column.
- Bind `Date.Date` (real date) and resample.
- Use `pd.Categorical(..., categories=[Jan, Feb, ...], ordered=True)`.

## Reference

- `../../examples/visual/ytd-line-chart.json`
