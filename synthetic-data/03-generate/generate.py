#!/usr/bin/env python3
"""
Config-driven star-schema synthetic data generator.

One YAML config declares DIMENSIONS and FACTS. Facts carry MEASURES with a top-line
`total` and `shares` per dimension/attribute; the engine allocates the total across the
grain (outer-product of the per-dimension share vectors), adds controlled noise, applies
sparsity, then RAKES (iterative proportional fitting) so every declared 1-D marginal ties
back exactly. Result: totals reconcile at every granularity (day, month, region, product…).

Usage:
    python generate.py <config.yaml> [--out DIR] [--archive]

Reusable across domains (retail, telecom, finance, web…) — change only the config.
Deps: pyyaml, numpy, pandas. Faker optional (attribute text). See ./engine-share-allocation.md
and ../02-schema/config-schema.md.
"""
from __future__ import annotations
import sys, os, json, argparse, datetime as dt
import numpy as np
import pandas as pd
try:
    import yaml
except ImportError:
    sys.exit("pip install pyyaml numpy pandas   (Faker optional)")
try:
    from faker import Faker
except ImportError:
    Faker = None

# retail-like default 12-month seasonal weights (Jan..Dec), peaks in Nov/Dec
SEASONAL = np.array([0.072,0.068,0.078,0.079,0.083,0.080,0.082,0.083,0.084,0.090,0.098,0.103])
SEASONAL = SEASONAL / SEASONAL.sum()


# ---------- dimensions ----------
def build_calendar(spec):
    lo, hi = [pd.Timestamp(x) for x in spec["range"]]
    days = pd.date_range(lo, hi, freq="D")
    df = pd.DataFrame({"Date": days})
    df["DateKey"] = df["Date"].dt.strftime("%Y%m%d").astype(int)
    df["Year"] = df["Date"].dt.year
    df["Quarter"] = "Q" + df["Date"].dt.quarter.astype(str)
    df["Month"] = df["Date"].dt.month
    df["MonthName"] = df["Date"].dt.strftime("%b")
    df["DayName"] = df["Date"].dt.strftime("%a")
    df["DayNum"] = df["Date"].dt.dayofweek + 1                 # sort-by for DayName (Mon=1)
    df["YearMonth"] = df["Date"].dt.year * 100 + df["Date"].dt.month   # sort-by for MonthYear
    df["MonthYear"] = df["Date"].dt.strftime("%b %Y")
    df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")
    return df, "DateKey"


def build_members(name, spec, rng, faker):
    key = spec.get("key", name + "Key")
    if "members" in spec:
        mem = spec["members"]
        rows = [{name: m} if not isinstance(m, dict) else dict(m) for m in mem]
        df = pd.DataFrame(rows)
        if name not in df.columns:  # a dict member must still expose the label col
            df[name] = df.iloc[:, 0]
    else:  # generate: N
        n = int(spec["generate"])
        df = pd.DataFrame({name: [f"{name}-{i:04d}" for i in range(1, n + 1)]})
        for attr, aspec in (spec.get("attributes") or {}).items():
            if "values" in aspec:
                w = aspec.get("weights")
                w = np.array(w, float) / np.sum(w) if w else None
                df[attr] = rng.choice(aspec["values"], size=n, p=w)
            elif "faker" in aspec and faker:
                fn = getattr(faker, aspec["faker"])
                df[attr] = [fn() for _ in range(n)]
            elif "min" in aspec:
                df[attr] = rng.integers(aspec["min"], aspec["max"] + 1, n)
    df.insert(0, key, range(1, len(df) + 1))
    return df, key


def build_dimensions(cfg, rng, faker):
    dims = {}
    for name, spec in cfg["dimensions"].items():
        if spec.get("type") == "calendar":
            df, key = build_calendar(spec)
        else:
            df, key = build_members(name, spec, rng, faker)
        dims[name] = {"df": df, "key": key, "label": name}
    return dims


# ---------- share resolution ----------
def share_vector(dimname, dim, shares, trend, rng):
    """Weight array aligned to dim['df'] rows, summing to 1.

    Multiple share blocks may target ONE dimension (e.g. Category dict + Item pareto):
    - CURVE specs (`seasonal`, `pareto`, `[list]`, extra dicts) multiply together and
      shape the distribution WITHIN groups.
    - The first DICT spec is the EXACT block: curves are normalized inside each of its
      groups, then scaled to the group's declared share — so group marginals pin exactly
      while curves still rank the members inside them.
    """
    df = dim["df"]; n = len(df)
    curves = np.ones(n); exact = None
    cols = [dimname] + [c for c in df.columns if c != dimname]
    for col in cols:
        if col not in shares:
            continue
        val = shares[col]
        if isinstance(val, dict):
            if exact is None:
                exact = (col, val)
            else:  # a second dict on the same dim only shapes (documented approximation)
                w = df[col].map(lambda x: val.get(x, np.nan)).to_numpy(float)
                fill = np.nanmean(w) if not np.isnan(w).all() else 1.0
                curves = curves * np.where(np.isnan(w), fill, w)
        elif val == "seasonal" and col in ("Month", "MonthName"):
            months = df["Month"].to_numpy() if "Month" in df.columns else np.arange(1, n + 1)
            curves = curves * SEASONAL[(months - 1) % 12]
        elif val == "pareto":
            curves = curves * (1.0 / np.arange(1, n + 1))  # 1/rank in member order
        elif isinstance(val, (list, tuple)):
            curves = curves * np.resize(np.array(val, float), n)
    # year-over-year trend on the calendar dim (a curve)
    if trend and "Year" in df.columns and trend.get("yoy"):
        yrs = df["Year"].to_numpy()
        curves = curves * np.power(1.0 + float(trend["yoy"]), (yrs - yrs.min()))
    if exact:
        col, val = exact
        key = df[col].to_numpy()
        gshare = df[col].map(lambda x: val.get(x, np.nan)).to_numpy(float)
        miss = np.isnan(gshare)
        if miss.any():  # undeclared groups split the remaining share evenly
            declared = sum(v for v in val.values())
            groups = pd.unique(df.loc[miss, col])
            per = max(0.0, 1.0 - declared) / len(groups) if len(groups) else 0.0
            gshare = np.where(miss, per, gshare)
        gsum = pd.Series(curves).groupby(key).transform("sum").to_numpy()
        w = np.where(gsum > 0, curves / gsum, 0.0) * gshare
    else:
        w = curves
    s = w.sum()
    return w / s if s > 0 else np.ones(n) / n


# ---------- allocation + raking ----------
def rake(df, grain, targets, iters=40, tol=1e-6):
    """Iterative proportional fitting: scale 'value' so each dim's marginal == target."""
    v = df["value"].to_numpy(float)
    for _ in range(iters):
        maxrel = 0.0
        for d in grain:
            key = df[d].to_numpy()
            cur = pd.Series(v).groupby(key).transform("sum").to_numpy()
            tgt = df[d].map(targets[d]).to_numpy(float)
            with np.errstate(divide="ignore", invalid="ignore"):
                factor = np.where(cur > 0, tgt / cur, 1.0)
            v = v * factor
            maxrel = max(maxrel, np.nanmax(np.abs(factor - 1.0)))
        if maxrel < tol:
            break
    df["value"] = v
    return df


def build_fact(fname, fspec, dims, rng):
    grain = fspec["grain"]
    labels = {d: dims[d]["label"] for d in grain}
    # cross product of member labels, then apply sparsity ONCE (shared row set for all measures)
    idx = pd.MultiIndex.from_product([dims[d]["df"][labels[d]] for d in grain], names=grain)
    out = idx.to_frame(index=False)
    sp = float(fspec.get("sparsity", 0.0))
    if sp > 0:
        out = out[rng.random(len(out)) >= sp].reset_index(drop=True)

    for mname, mspec in fspec["measures"].items():
        if "derived" in mspec:
            continue
        total = float(mspec["total"]); shares = mspec.get("shares", {})
        trend = mspec.get("trend"); noise = float(mspec.get("noise", 0.0))
        # per-dim weight vectors (member -> share), summing to 1
        wv = {d: pd.Series(share_vector(d, dims[d], shares, trend, rng),
                           index=dims[d]["df"][labels[d]].to_numpy()) for d in grain}
        # expected value per cell = total x product of the per-dim shares (outer product)
        exp = np.full(len(out), total, float)
        for d in grain:
            exp = exp * out[d].map(wv[d]).to_numpy(float)
        if noise > 0:  # mean-preserving lognormal jitter
            exp = exp * rng.lognormal(-0.5 * noise * noise, noise, len(out))
        if "max" in mspec: exp = np.minimum(exp, float(mspec["max"]))
        if "min" in mspec: exp = np.maximum(exp, float(mspec["min"]))
        work = out[grain].copy(); work["value"] = exp
        # rake to exact declared 1-D marginals (total x share per member)
        targets = {d: (total * wv[d]).to_dict() for d in grain}
        work = rake(work, grain, targets)
        out[mname] = work["value"].to_numpy()

    # derived measures (evaluated over the row set; params sampled per row)
    for mname, mspec in fspec["measures"].items():
        if "derived" not in mspec:
            continue
        params = {k: rng.uniform(v["min"], v["max"], len(out)) for k, v in mspec.items()
                  if isinstance(v, dict) and "min" in v}
        env = {**{c: out[c].to_numpy(float) for c in out.columns if out[c].dtype.kind in "fi"},
               **params, "round": np.round, "np": np}
        out[mname] = eval(mspec["derived"], {"__builtins__": {}}, env)  # noqa: config-controlled expr

    # swap member labels for surrogate FKs
    for d in grain:
        dd = dims[d]
        out = out.merge(dd["df"][[dd["key"], labels[d]]], on=labels[d], how="left").drop(columns=[labels[d]])
    out.insert(0, fname + "Key", range(1, len(out) + 1))
    return out


# ---------- main ----------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("config")
    ap.add_argument("--out", default=None)
    ap.add_argument("--archive", action="store_true")
    a = ap.parse_args()
    cfg = yaml.safe_load(open(a.config, encoding="utf-8"))
    seed = int(cfg.get("seed", 42))
    rng = np.random.default_rng(seed)
    faker = None
    if Faker:
        faker = Faker(); faker.seed_instance(seed)

    dims = build_dimensions(cfg, rng, faker)
    facts = {fn: build_fact(fn, fs, dims, rng) for fn, fs in cfg["facts"].items()}

    outdir = a.out or (cfg.get("output", {}).get("dir") or f"outputs/{cfg.get('name','job')}/latest")
    os.makedirs(outdir, exist_ok=True)
    manifest = {"generated": dt.datetime.now().isoformat(timespec="seconds"),
                "seed": seed, "config": os.path.basename(a.config), "tables": {}}
    for name, d in dims.items():
        p = os.path.join(outdir, f"Dim{name}.csv"); d["df"].to_csv(p, index=False)
        manifest["tables"][f"Dim{name}"] = len(d["df"])
    for name, f in facts.items():
        p = os.path.join(outdir, f"Fact{name}.csv"); f.to_csv(p, index=False)
        manifest["tables"][f"Fact{name}"] = len(f)
    json.dump(manifest, open(os.path.join(outdir, "_manifest.json"), "w"), indent=2)
    print(f"[ok] wrote {len(dims)} dims + {len(facts)} facts to {outdir}")
    for t, n in manifest["tables"].items():
        print(f"      {t}: {n:,} rows")


if __name__ == "__main__":
    main()
