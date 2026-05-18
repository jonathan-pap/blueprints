# Enable R scripting in PBI Desktop

One-time per machine.

## Steps

1. Install R from CRAN.
2. Install required packages: `install.packages(c("ggplot2","dplyr","scales"))`.
3. In Power BI Desktop: File → Options → R scripting.
4. Set "Detected R home directories" to the R install.
5. Restart Desktop.

## Verify

Add an R visual to a page. Bind any field. The script editor shows:

```r
# dataset <- data.frame(<your fields>)
# dataset <- unique(dataset)
```

If you see that, R is wired. If "R script returned no images", check `library(ggplot2)` works in that R install.

## Common pitfalls

- Power BI uses ONE R install at a time — switching between forks (CRAN R, Microsoft R Open, Pro R) requires Desktop restart.
- Packages must be in the configured R's library — `.libPaths()` from within Desktop's R env to verify.
- Conda's R is not Power BI's R. Don't confuse them.

## See also

- `common-pitfalls.md` — runtime issues
- `bind-dataset.md` — what `dataset` looks like
