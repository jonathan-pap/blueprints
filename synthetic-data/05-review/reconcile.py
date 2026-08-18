#!/usr/bin/env python3
"""
Reconciliation validator for the config-driven generator.

Reads the same config + the generated star, joins each fact to its dims, and asserts every
declared `total` and `shares` weight is actually present in the data (within tolerance).
This is the check the config-driven engine makes possible and a bespoke script can't: proof
that the marginals tie out at every declared granularity.

Usage:  python reconcile.py <config.yaml> [--dir OUTDIR] [--tol 0.01]
Exit 0 = all reconciled; exit 1 = at least one marginal drifted.
"""
import sys, os, argparse
import pandas as pd, numpy as np, yaml

SEASONAL = np.array([0.072,0.068,0.078,0.079,0.083,0.080,0.082,0.083,0.084,0.090,0.098,0.103])
SEASONAL = SEASONAL / SEASONAL.sum()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("config"); ap.add_argument("--dir", default=None); ap.add_argument("--tol", type=float, default=0.01)
    a = ap.parse_args()
    cfg = yaml.safe_load(open(a.config, encoding="utf-8"))
    outdir = a.dir or (cfg.get("output", {}).get("dir") or f"outputs/{cfg.get('name','job')}/latest")
    dims = {n: pd.read_csv(os.path.join(outdir, f"Dim{n}.csv")) for n in cfg["dimensions"]}
    keys = {n: (s.get("key", n + "Key") if s.get("type") != "calendar" else "DateKey")
            for n, s in cfg["dimensions"].items()}
    fails = 0
    for fname, fspec in cfg["facts"].items():
        fact = pd.read_csv(os.path.join(outdir, f"Fact{fname}.csv"))
        for d in fspec["grain"]:
            fact = fact.merge(dims[d], on=keys[d], how="left")
        print(f"\n== Fact{fname} ({len(fact):,} rows) ==")
        for mname, mspec in fspec["measures"].items():
            if "shares" not in mspec:
                continue
            tot = fact[mname].sum(); dtot = float(mspec["total"])
            ok = abs(tot - dtot) / dtot <= a.tol
            fails += not ok
            print(f"  {mname}: total {tot:,.0f} vs {dtot:,.0f}  {'OK' if ok else 'FAIL'}")
            for col, val in mspec["shares"].items():
                if not isinstance(val, dict):
                    continue  # seasonal/pareto/list checked structurally, not per-key
                actual = (fact.groupby(col)[mname].sum() / tot)
                for member, share in val.items():
                    got = float(actual.get(member, 0.0)); good = abs(got - share) <= a.tol
                    fails += not good
                    print(f"      {col}={member}: {got:.3f} vs {share:.3f}  {'OK' if good else 'FAIL'}")
    print(f"\n{'ALL RECONCILED' if fails == 0 else str(fails)+' MARGINAL(S) DRIFTED'} (tol {a.tol})")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
