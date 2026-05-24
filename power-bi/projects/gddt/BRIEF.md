# gddt Delivery Tracker — Views Brief

> Status: **draft v1** · 2026-05-21 · Scope: report information architecture (10,000 ft → file detail)

Purpose: scope the delivery-tracking report into layered views and pin down
**where the data lives** at each level, so the build is deliberate rather than
ad-hoc.

---

## 1. Where the data is

| Table | Role | Grain | Key fields |
|---|---|---|---|
| **`expected`** (expected.csv) | The **plan / denominator** — what *should* arrive | 1 row per `hash_id` × period | `domain · group · dataset_name · dc_name` (contract) · `entity · frequency`; `year/month → period_date` (active → calendar); `deadline_date` = **15th** of the month |
| **`fct_delivery`** (fct_delivery.csv) | The **actuals + pipeline** | 1 row per delivery *attempt*; `is_active` = latest per hash | `status_3_on_time → 4_schema_failed → 5_quar_scope → 6_quar_time → 7_dq_records → 8_bus_approved → 9_reached_gold`; `insp_record_count`; `received_ts_rai → received_date` (inactive → calendar) |
| **`dim_calendar`** | Time spine | per day | active on `expected[period_date]`; inactive on `fct_delivery[received_date]` |
| **`_Measures`** | Semantic layer | — | counts, rates, daily flow |

**Join model:** there is *no* physical `expected ↔ fct_delivery` relationship —
measures match by `hash_id IN <set of delivered hashes>`.

---

## 2. The pipeline (the path every file walks)

```
Expected → Received → On-time? → Schema OK? → Quarantine (scope / time)?
        → DQ records? → Business approved? → Reached Gold
```

Deadline = the **15th** of the reporting month.
Past deadline + not received = **Overdue**. Before deadline + not received = **Pending**.

---

## 3. Layered views

| Level | Audience | Answers | Key visuals | Data / measures |
|---|---|---|---|---|
| **L0 · 10,000 ft — Health** | Leadership | Are we on track this period? | KPI cards (# Expected, % Delivered, % On Time, % Reached Gold, # Overdue) + month-by-month **stacked bar** + %-Gold trend | rates + counts over `period_date` |
| **L1 · 5,000 ft — Where's the problem** | Domain stewards | Which domain / group / dataset / contract is behind? | Matrix `domain ▸ group ▸ dataset` × state counts (conditional format) + overdue-by-group bar; slicers: period, domain, group, frequency | `expected` dims × status measures |
| **L2 · 1,000 ft — Pipeline funnel** | Data engineers | Where do files drop off? | Funnel `Expected → Delivered → On-time → Schema OK → Past Quarantine → DQ OK → Approved → Gold` + quarantine breakdown | `fct_delivery[status_3..9]`, `is_active` |
| **L2.5 · Daily ops** | Platform on-call | What landed today / MTD vs due? | `# Received Today`, `# Received MTD`, `# Expected by Day` line | `received_date` (USERELATIONSHIP) |
| **L3 · Ground — File detail** | Investigator | *Exactly* which files are overdue / failed? | Drill-through table: hash, contract, dataset, group, deadline, received, current state, all flags, # attempts | `expected` ⨝ active `fct_delivery` by `hash_id` |

---

## 4. Modeling fixes the views depend on

1. **One canonical `CurrentState` per file** — *critical for L0 and L2.* Today each
   status measure counts independently, so a file that is both `on_time` **and**
   `reached_gold` is counted in **both** buckets → the stacked bar exceeds Expected
   (the observed ~208 vs 104). Define a single state via a priority `SWITCH`, then
   count **distinct hashes per state** so the stack partitions to Expected.
2. **`DISTINCTCOUNT(expected[hash_id])`** as the base for `# Expected` / status
   counts — guards against `expected` carrying >1 row per hash in the filter
   context (multi-month or CSV duplicates).
3. *(Optional)* a real `expected[hash_id] ↔ fct_delivery` relationship or bridge —
   faster than `IN`-set logic and enables natural cross-filtering at L3.

---

## 5. Open decisions (to confirm before locking v1)

- **`CurrentState` priority order** — proposed:
  `Reached Gold ▸ Business Approved ▸ DQ records found ▸ Quarantine (scope) ▸
  Quarantine (time) ▸ Schema failed ▸ On-time / Delivered ▸ Overdue ▸ Pending`.
  Confirm this matches governance.
- **Level cut** — keep all 5 levels, or trim?
- **Period** — report by `period_date` (expected month) everywhere?
