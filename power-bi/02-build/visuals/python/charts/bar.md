# Python — bar chart

## Bindings

```bash
pbir visuals bind "<...>/MyPyBar.Visual" \
  -a "Values:Geography.Region" -t Column \
  -a "Values:Sales.Revenue"    -t Measure
```

## Script

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(8, 4))
data = dataset.sort_values("Revenue", ascending=True)
ax.barh(data["Region"], data["Revenue"], color="#118DFF")
ax.set_xlabel("Revenue")
ax.set_title("Revenue by Region")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.tight_layout()
plt.show()
```

## Why horizontal

Long region names fit better horizontally. For short labels use vertical with `ax.bar(...)`.

## Sort descending

`sort_values(..., ascending=True)` because `barh` plots bottom-up; this makes the largest bar appear on top.

## Reference

- `../../examples/script/bar-chart.py` — fuller example
- `../../examples/visual/bar-chart.json` — full PBIR visual block
