# projects/ — raw layer

One folder per generation job. The working files for producing a dataset live here; the dated
results land in `../outputs/`.

```text
projects/<job-name>/
├── brief.md            what data, why, volume, seed, output target   (from 01-brief)
├── schema.<ext>        the data definition                            (from 02-schema)
├── generate.py         the generator script                           (from 03-generate)
└── seed.txt            recorded RNG seed for reproducibility
```

Keep job names kebab-case (e.g. `demo-financials`, `loadtest-orders`). Generators are
re-runnable: same seed + same schema reproduces the same data.
