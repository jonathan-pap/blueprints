# Brief template

Copy this file to `projects/<job-name>/brief.md` and fill in the bracketed sections. Delete what
doesn't apply. The agent reads this BEFORE asking you questions.

---

```markdown
# Brief — <Job Name>

Last updated: YYYY-MM-DD

## 1. Purpose & consumer

- **Purpose:** [demo / functional test / load test / ML fixture / populate a BI model]
- **Who/what consumes it:** [a Power BI model / a test suite / a notebook / a person eyeballing it]
- **Realism level:** [random-but-valid / business-plausible distributions / mimic a real dataset's shape]

## 2. Datasets & volume

| Entity / table | Rows | Notes |
|---|---|---|
| customers | 5,000 | parent |
| orders | 50,000 | child of customers |
| [...] | [...] | [...] |

## 3. Schema source

- [ ] From scratch (describe fields in §4 or in `schema.<ext>`)
- [ ] Match an existing schema: [path / table name]
- [ ] Mimic the *shape* of a real dataset (privacy-safe, distributions only): [source]

## 4. Fields, types & distributions

Per entity — name, type, domain, distribution, null rate. (Full detail lives in `02-schema/`.)

| Field | Type | Domain / pattern | Distribution | Null % |
|---|---|---|---|---|
| email | string | faker.email | — | 0 |
| sales | decimal | 0–100000 | right-skewed | 2 |
| segment | category | {SMB, Mid, Ent} | weighted 60/30/10 | 0 |
| [...] | [...] | [...] | [...] | [...] |

## 5. Constraints & relationships

- **Keys:** [primary keys; uniqueness]
- **Relationships:** [foreign keys, cardinality — e.g. orders.customer_id → customers.id]
- **Business rules:** [cross-field, e.g. `ship_date >= order_date`, `total = qty * price`]
- **Temporal:** [date range, trend, seasonality]

## 6. Reproducibility

- **Seed:** [integer — record it; same seed + same schema = same data] (default: yes, fix a seed)

## 7. Privacy / PII

- **Synthetic only.** No real records or real PII as input or output.
- If mimicking real data: learn distributions/structure only — never copy rows through.

## 8. Output target

- **Format(s):** [CSV / JSON / NDJSON / Parquet / SQL INSERT / DB load]
- **Destination:** [outputs/ / a database / a Power BI project]
- **Power BI hand-off?** [no / yes → target `../power-bi/projects/<name>/` — see 04-output/handoff-to-power-bi.md]

## 9. Open questions

- [ ] [anything you're unsure about — the agent surfaces these first instead of guessing]
```

---

## After filling this in

1. Save to `projects/<job-name>/brief.md` (or split into `projects/<job-name>/brief/*.md`).
2. Tell Claude the intent (e.g. "generate the data"). The agent reads the brief, fills gaps via
   `AskUserQuestion`, then enters `02-schema/` → `03-generate/` → `04-output/` → `05-review/`.
3. Keep the brief updated — it's the source of truth for why the dataset looks the way it does.
