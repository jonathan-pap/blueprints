# Enable Python scripting in PBI Desktop

One-time setup per machine.

## Steps

1. Install a Python distribution (Anaconda Miniconda or python.org).
2. Install required packages: `pip install pandas matplotlib seaborn`.
3. In Power BI Desktop: File → Options → Python scripting.
4. Set "Detected Python home directories" to the env that has the packages.
5. Restart Desktop.

## Verify

Add a Python visual to a page. Bind any field. The script editor should show:

```python
# The following code to create a dataframe and remove duplicated rows is always executed and acts as a preamble for your script:
# dataset = pandas.DataFrame(<your fields>)
# dataset = dataset.drop_duplicates()
```

If you see that, Python is wired up. If you see "Python script returned no images", check that the env has matplotlib.

## Common pitfalls

- Conda envs need to be activated outside Desktop too — easiest is to set system PATH to the env or use the `python.exe` direct path.
- Updating packages requires Desktop restart.
- The Python env in Desktop is process-isolated; it can't access your user's `site-packages` unless they're in the configured env.

## See also

- `common-pitfalls.md` — runtime issues
- `bind-dataset.md` — what `dataset` looks like
