# R — bullet chart (ggplot2)

R is good at bullet charts because ggplot2's layered grammar matches the bullet structure cleanly (three bands + actual + target tick).

## Bindings

```bash
pbir visuals bind "<...>/MyRBullet.Visual" \
  -a "Values:Geography.Region"       -t Column \
  -a "Values:Sales.Revenue"          -t Measure \
  -a "Values:Sales.Revenue Target"   -t Measure \
  -a "Values:Sales.Revenue 50pct"    -t Measure \
  -a "Values:Sales.Revenue 80pct"    -t Measure \
  -a "Values:Sales.Revenue 100pct"   -t Measure
```

## Script (see `examples/visual/bullet-chart.json` for full)

```r
library(ggplot2)

p <- ggplot(dataset, aes(y = Region)) +
  geom_col(aes(x = `Revenue 100pct`), fill = "#E5E5E5") +
  geom_col(aes(x = `Revenue 80pct`),  fill = "#CCCCCC") +
  geom_col(aes(x = `Revenue 50pct`),  fill = "#999999") +
  geom_col(aes(x = Revenue),          fill = "#118DFF", width = 0.4) +
  geom_segment(aes(x = `Revenue Target`, xend = `Revenue Target`,
                   y = as.numeric(factor(Region)) - 0.4,
                   yend = as.numeric(factor(Region)) + 0.4),
               color = "black", linewidth = 0.8) +
  labs(x = "Revenue", y = NULL) +
  theme_minimal()

print(p)
```

## Reads as

Three light-to-dark gray bands (target ranges), one blue actual bar (thinner), one black target tick. Reader sees where actual falls in the range bands.

## Reference

- `../../examples/visual/bullet-chart.json`
