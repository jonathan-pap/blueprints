"""Fetch orbital launches from The Space Devs' Launch Library 2 into the EXISTING schema.

The report's model, its 23 measures and every visual are bound to the nine columns of
`space_missions_clean.csv`. This script is therefore written to one hard constraint:

    emit those nine columns, in the same formats, and nothing else.

    Company, Location, Date, Time, Rocket, Mission, RocketStatus, Price, MissionStatus

LL2 goes back to Sputnik 1 (1957-10-04) and is current to today, so this REPLACES the
dataset rather than extending it - which is what avoids reconciling two sources' operator
names against each other.

Usage
-----
    python fetch_ll2.py --pilot 2024              # one year, prints rows, writes nothing
    python fetch_ll2.py --out space_missions_ll2.csv
    python fetch_ll2.py --out ... --resume        # continue an interrupted pull

Notes
-----
* Only COMPLETED launches are taken (`status__ids=3,4,7`). LL2 also carries scheduled
  launches out to 2039 with status TBD; including them would project empty columns into
  the 2030s.
* Unauthenticated LL2 allows ~15 requests/hour. A full pull is ~76 pages, so it either
  needs an API key (`--key`) or several passes with `--resume`.
* LL2 is free for non-commercial use, with attribution.
"""
import argparse
import csv
import json
import os
import sys
import time
import urllib.parse
import urllib.request

API = "https://ll.thespacedevs.com/2.2.0/launch/"
COLUMNS = ["Company", "Location", "Date", "Time", "Rocket", "Mission",
           "RocketStatus", "Price", "MissionStatus"]

# LL2 spells operators out in full; the existing dataset uses the short forms that read
# well in a Top-5 bar list. Anything not listed here passes through unchanged and is
# reported at the end so the mapping can be extended deliberately rather than guessed.
PROVIDER = {
    "China Aerospace Science and Technology Corporation": "CASC",
    "Russian Federal Space Agency (ROSCOSMOS)": "Roscosmos",
    "Russian Space Forces": "VKS RF",
    "Soviet Space Program": "RVSN USSR",
    "Strategic Rocket Forces": "RVSN USSR",
    "Indian Space Research Organization": "ISRO",
    "United Launch Alliance": "ULA",
    "National Aeronautics and Space Administration": "NASA",
    "Mitsubishi Heavy Industries": "MHI",
    "Northrop Grumman": "Northrop",
    "Northrop Grumman Innovation Systems": "Northrop",
    "Orbital Sciences Corporation": "Northrop",
    "Lockheed Martin": "Lockheed",
    "Lockheed Martin Space": "Lockheed",
    "Martin Marietta": "Martin Marietta",
    "General Dynamics": "General Dynamics",
    "United States Air Force": "US Air Force",
    "United States Navy": "US Navy",
    "Japan Aerospace Exploration Agency": "JAXA",
    "European Space Agency": "ESA",
    "China Aerospace Science and Industry Corporation": "CASIC",
    "Israeli Space Agency": "ISA",
    "Korea Aerospace Research Institute": "KARI",
    # operators new since 2022 whose full names would swamp a Top-5 bar list
    "Islamic Revolutionary Guard Corps Aerospace Force": "IRGC ASF",
    "Khrunichev State Research and Production Space Center": "Khrunichev",
    "National Aerospace Development Administration": "NADA",
    "China Rocket Co. Ltd.": "China Rocket",
    "Orienspace Technology": "Orienspace",
}

# LL2 status abbrev -> the four values MissionStatus already uses.
STATUS = {
    "Success": "Success",
    "Failure": "Failure",
    "Partial Failure": "Partial Failure",
    "Prelaunch Failure": "Prelaunch Failure",
}


def get(url, key=None, retries=4):
    """GET with backoff. LL2 answers 429 when the hourly budget is spent."""
    # LL2 rejects the default python-urllib agent with 403; any real UA is accepted
    req = urllib.request.Request(url, headers={
        "Accept": "application/json",
        "User-Agent": "space-launch-cadence/1.0 (PBI report data pull)",
    })
    if key:
        req.add_header("Authorization", f"Token {key}")
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = 60 * (attempt + 1)
                print(f"    rate-limited; sleeping {wait}s", file=sys.stderr)
                time.sleep(wait)
                continue
            raise
        except Exception:
            if attempt == retries - 1:
                raise
            time.sleep(5 * (attempt + 1))
    raise RuntimeError("exhausted retries")


def to_row(r, unmapped):
    """Map one LL2 launch onto the nine existing columns."""
    cfg = ((r.get("rocket") or {}).get("configuration") or {})
    pad = r.get("pad") or {}
    loc = (pad.get("location") or {}).get("name") or ""

    provider = (r.get("launch_service_provider") or {}).get("name") or ""
    company = PROVIDER.get(provider, provider)
    if provider and provider not in PROVIDER:
        unmapped[provider] = unmapped.get(provider, 0) + 1

    # existing Location is a comma-joined "pad, place" string
    location = ", ".join(p for p in (pad.get("name"), loc) if p)

    net = r.get("net") or ""                      # 2024-03-05T12:34:56Z
    date, _, rest = net.partition("T")
    tm = rest[:8] if len(rest) >= 8 else ""       # HH:MM:SS, blank if unknown

    # existing Price is millions of USD; LL2 launch_cost is whole USD
    cost = cfg.get("launch_cost")
    try:
        price = f"{int(cost) / 1_000_000:g}" if cost else ""
    except (TypeError, ValueError):
        price = ""

    return {
        "Company": company,
        "Location": location,
        "Date": date,
        "Time": tm,
        "Rocket": cfg.get("full_name") or cfg.get("name") or "",
        "Mission": (r.get("mission") or {}).get("name") or "",
        "RocketStatus": "Active" if cfg.get("active") else "Retired",
        "Price": price,
        "MissionStatus": STATUS.get((r.get("status") or {}).get("abbrev"), ""),
    }


def fetch(out, key=None, limit=100, resume=False, pilot=None):
    params = {"limit": limit, "ordering": "net", "mode": "detailed",
              "status__ids": "3,4,7"}
    if pilot:
        params["net__gte"] = f"{pilot}-01-01"
        params["net__lte"] = f"{pilot}-12-31"

    cache = (out or "ll2") + ".partial.json"
    rows, offset = [], 0
    if resume and os.path.exists(cache):
        saved = json.load(open(cache, encoding="utf-8"))
        rows, offset = saved["rows"], saved["offset"]
        print(f"resuming at offset {offset} ({len(rows)} rows cached)")

    unmapped, total = {}, None
    while True:
        params["offset"] = offset
        data = get(API + "?" + urllib.parse.urlencode(params), key)
        total = data.get("count")
        batch = data.get("results") or []
        if not batch:
            break
        rows.extend(to_row(r, unmapped) for r in batch)
        offset += len(batch)
        print(f"  {offset}/{total}")
        if pilot and offset >= (total or 0):
            break
        if offset >= (total or 0):
            break
        if not pilot:
            json.dump({"rows": rows, "offset": offset}, open(cache, "w", encoding="utf-8"))
            time.sleep(2)

    return rows, total, unmapped


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", help="CSV path to write")
    ap.add_argument("--key", help="LL2 API token (lifts the ~15/hour limit)")
    ap.add_argument("--pilot", type=int, help="fetch a single year and print it")
    ap.add_argument("--resume", action="store_true")
    a = ap.parse_args()

    rows, total, unmapped = fetch(a.out, a.key, resume=a.resume, pilot=a.pilot)
    print(f"\nfetched {len(rows)} completed launches (API reports {total})")

    # Only names that do not already exist in the current dataset matter - anything that
    # matches is fine as-is, mapped or not.
    existing = set()
    cur = os.path.join(os.path.dirname(os.path.abspath(__file__)), "space_missions_clean.csv")
    if os.path.exists(cur):
        with open(cur, encoding="utf-8") as f:
            existing = {r["Company"] for r in csv.DictReader(f)}
    produced = {r["Company"] for r in rows}
    novel = sorted(produced - existing) if existing else []
    if novel:
        print(f"\n{len(novel)} operator name(s) NOT present in the current dataset:")
        counts = {}
        for r in rows:
            counts[r["Company"]] = counts.get(r["Company"], 0) + 1
        for name in sorted(novel, key=lambda n: -counts[n]):
            print(f"  {counts[name]:5}  {name}")
        print("  -> genuinely new operators are expected; a LONG name here means it needs")
        print("     a short form in PROVIDER so Top-5 lists stay readable")
    elif existing:
        print("\nevery operator name matches one already in the dataset")

    if a.pilot:
        print(f"\nsample rows for {a.pilot} in the existing schema:")
        w = csv.DictWriter(sys.stdout, fieldnames=COLUMNS, lineterminator="\n")
        w.writeheader()
        for r in rows[:8]:
            w.writerow(r)
        return

    if a.out:
        with open(a.out, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=COLUMNS, lineterminator="\n")
            w.writeheader()
            w.writerows(rows)
        print(f"wrote {a.out}")
        cache = a.out + ".partial.json"
        if os.path.exists(cache):
            os.remove(cache)


if __name__ == "__main__":
    main()
