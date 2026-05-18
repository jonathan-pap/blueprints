# Python visual pitfalls

## 1. Missing package = silent failure

The script runs in PBI's chosen Python env. A missing import returns "Python script returned no images" with no detail.

Fix: install the package via the exact env Desktop uses. Verify with `pip list` in that env.

## 2. Randomness without a seed

Power BI re-runs the script on every filter change. Without `numpy.random.seed(42)`, the visual flickers different shapes each interaction.

Fix: always seed random ops.

## 3. Multiple figures

Power BI captures the LAST `matplotlib.pyplot` figure. Multiple `plt.show()` calls drop earlier figures.

Fix: build one figure with `plt.subplots()` if you need multiple plots.

## 4. Output isn't a figure

`plt.plot(...)` alone doesn't always trigger figure capture. Be explicit:

```python
fig, ax = plt.subplots()
ax.plot(dataset['Month'], dataset['Revenue'])
plt.show()
```

## 5. Theme colors

Python visuals don't read the Power BI theme. Hardcode your palette to match the theme manually, or pass colors via a thin-report measure bound as a field — clunky but works for sentiment.

## 6. 150k row default limit

Above 150k rows, Power BI samples. Results are non-deterministic. If you need precise stats, pre-aggregate in the model.

## 7. Slow on filter

Python visuals re-render the full script on every filter change. Avoid heavy computation; pre-aggregate where possible.

## 8. No interactivity

Output is a PNG. No cross-filter, no hover, no click. If interactivity matters, use Deneb (`../../deneb/`).
