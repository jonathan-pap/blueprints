# R — trend line (ggplot2)

## Bindings

```bash
pbir visuals bind "<...>/MyRTrend.Visual" \
  -a "Values:Date.Month"    -t Column \
  -a "Values:Sales.Revenue" -t Measure
```

## Script

```r
library(ggplot2)
library(dplyr)

data <- dataset %>%
  mutate(Month = as.Date(Month)) %>%
  arrange(Month)

p <- ggplot(data, aes(x = Month, y = Revenue)) +
  geom_line(color = "#118DFF", linewidth = 1) +
  geom_point(color = "#118DFF", size = 2) +
  labs(x = NULL, y = "Revenue") +
  theme_minimal() +
  theme(panel.grid.minor = element_blank())

print(p)
```

## Convert dates

If `Date.Month` comes through as text (PBI's Calendar Month columns sometimes do), `as.Date()` enforces ordering.

## Reference

- `../../examples/script/trend-line.R`
- `../../examples/visual/trend-line.json`
