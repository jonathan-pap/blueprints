# What is PBIP

The developer-mode file format for Power BI. Decomposes a `.pbix` binary into human-readable text files in folders.

```
<name>/
├── <name>.Report/         PBIR JSON (visuals, pages, theme refs)
├── <name>.SemanticModel/  TMDL (tables, measures, columns, relationships)
└── <name>.pbip            entry point opened by PBI Desktop
```

Open the project two ways: double-click `<name>.pbip`, or open `<name>.Report/definition/definition.pbir` directly. Both work; the `.pbip` file is optional.
