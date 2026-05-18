# R — bar chart (ggplot2)

## Bindings

```bash
pbir visuals bind "<...>/MyRBar.Visual" \
  -a "Values:Geography.Region" -t Column \
  -a "Values:Sales.Revenue"    -t Measure
```

## Script

```r
library(ggplot2)
library(dplyr)

data <- dataset %>% arrange(desc(Revenue))

p <- ggplot(data, aes(x = reorder(Region, Revenue), y = Revenue)) +
  geom_col(fill = "#118DFF") +
  coord_flip() +
  labs(title = NULL, x = NULL, y = "Revenue") +
  theme_minimal() +
  theme(panel.grid.major.y = element_blank(),
        panel.grid.minor   = element_blank())

print(p)
```

## Why horizontal

`coord_flip()` makes long region labels readable. For short labels, drop `coord_flip()` and you get a vertical column chart.

## Sort

`reorder(Region, Revenue)` orders the category axis by the measure value, ascending. Combined with `coord_flip()`, the largest bar appears at top.

## Reference

- `../../examples/script/bar-chart.R`
- `../../examples/visual/bar-chart.json`
