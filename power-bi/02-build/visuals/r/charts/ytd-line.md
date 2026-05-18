# R — YTD line (ggplot2)

Two lines: CY YTD vs PY YTD.

## Bindings

```bash
pbir visuals bind "<...>/MyRYtd.Visual" \
  -a "Values:Date.Calendar Month (ie Jan)" -t Column \
  -a "Values:Sales.Revenue YTD"             -t Measure \
  -a "Values:Sales.Revenue YTD PY"          -t Measure
```

## Script

```r
library(ggplot2)
library(dplyr)
library(tidyr)

data <- dataset %>%
  rename(Month = `Calendar Month (ie Jan)`, CY = `Revenue YTD`, PY = `Revenue YTD PY`) %>%
  mutate(Month = factor(Month, levels = month.abb, ordered = TRUE)) %>%
  pivot_longer(cols = c(CY, PY), names_to = "Series", values_to = "Value")

p <- ggplot(data, aes(x = Month, y = Value, color = Series, group = Series, linetype = Series)) +
  geom_line(linewidth = 1) +
  geom_point(size = 2) +
  scale_color_manual(values = c("CY" = "#118DFF", "PY" = "#CCCCCC")) +
  scale_linetype_manual(values = c("CY" = "solid", "PY" = "dashed")) +
  labs(x = NULL, y = "Revenue") +
  theme_minimal() +
  theme(legend.position = "top", legend.title = element_blank())

print(p)
```

## Month ordering

`factor(Month, levels = month.abb)` forces calendar order. Without it, ggplot defaults to alphabetical ("Apr, Aug, Dec...").

## Reference

- `../../examples/visual/ytd-line-chart.json`
