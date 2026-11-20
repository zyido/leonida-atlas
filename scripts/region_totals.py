#!/usr/bin/env python3
"""Per-region totals, and a check that they add up to the dataset total.

    python3 scripts/region_totals.py data/leonida.json

Region assignment is the final address label matched against the aliases in
data/regions.json — never a coordinate lookup. Anything whose label has no
mapping counts as unassigned, which is why the region totals are a floor
rather than a ceiling.
"""

import argparse
import collections
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from leonida import (  # noqa: E402
    alias_map, is_named, is_positioned, load_dataset, load_regions, region_of,
)

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_REGIONS = os.path.join(HERE, os.pardir, "data", "regions.json")


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("dataset", help="path to data/leonida.json")
    parser.add_argument(
        "--regions",
        default=DEFAULT_REGIONS,
        help="path to data/regions.json (default: %(default)s)",
    )
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    records = load_dataset(args.dataset)
    regions = load_regions(args.regions)
    aliases = alias_map(regions)

    totals = collections.defaultdict(lambda: {"total": 0, "positioned": 0, "named": 0})
    for record in records:
        slug = region_of(record, aliases) or "unassigned"
        bucket = totals[slug]
        bucket["total"] += 1
        bucket["positioned"] += 1 if is_positioned(record) else 0
        bucket["named"] += 1 if is_named(record) else 0

    order = [r["slug"] for r in regions.get("regions", [])] + ["unassigned"]
    names = {r["slug"]: r.get("name", r["slug"]) for r in regions.get("regions", [])}
    names["unassigned"] = "(no region label)"

    print(f"{'Region':<26}{'Total':>7}{'Positioned':>12}{'Named':>7}")
    for slug in order:
        bucket = totals[slug]
        print(
            f"{names.get(slug, slug):<26}{bucket['total']:>7}"
            f"{bucket['positioned']:>12}{bucket['named']:>7}"
        )

    counted = sum(totals[slug]["total"] for slug in order if slug in totals)
    print()
    print(f"Records counted: {counted} of {len(records)}")
    if counted != len(records):
        print("MISMATCH: some records landed in no bucket", file=sys.stderr)
        return 1

    # Cross-check against the published totals when they are present.
    published = {r["slug"]: r.get("totalCount") for r in regions.get("regions", [])}
    drifted = [
        (slug, totals[slug]["total"], published[slug])
        for slug in published
        if published[slug] is not None and totals[slug]["total"] != published[slug]
    ]
    if drifted:
        print("DRIFT against data/regions.json:", file=sys.stderr)
        for slug, actual, expected in drifted:
            print(f"  {slug}: dataset {actual}, regions.json {expected}", file=sys.stderr)
        return 1
    print("Matches the published totals in data/regions.json.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
