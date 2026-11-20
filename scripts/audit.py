#!/usr/bin/env python3
"""Reproduce the coverage table in README.md from the dataset itself.

    python3 scripts/audit.py data/leonida.json
    python3 scripts/audit.py data/leonida.json --table-only

Prints how many records exist, how many have a position, a name and a region,
then lists every record that is missing a position or a region so the gaps can
be checked instead of taken on trust.
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from leonida import (  # noqa: E402
    alias_map, coverage, is_named, is_positioned, load_dataset, load_regions,
    region_of, source_label,
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
    parser.add_argument(
        "--table-only",
        action="store_true",
        help="print the coverage table without the gap lists",
    )
    return parser.parse_args(argv)


def print_table(counts):
    rows = [
        ("Records in dataset", counts["total"]),
        ("Records with coordinates", counts["positioned"]),
        ("Records with a name", counts["named"]),
        ("Records with no location", counts["unpositioned"]),
        ("Records with no region", counts["unassigned"]),
    ]
    width = max(len(label) for label, _ in rows)
    for label, value in rows:
        print(f"  {label:<{width}}  {value:>6}")


def print_gaps(records, aliases):
    unpositioned = [r for r in records if not is_positioned(r)]
    unassigned = [r for r in records if not region_of(r, aliases)]

    print()
    print(f"Records with no location ({len(unpositioned)})")
    for record in unpositioned:
        print(f"  {record.get('id', '?'):<8} {source_label(record) or '(no label)'}")

    print()
    print(f"Records with no region ({len(unassigned)})")
    for record in unassigned:
        name = (record.get("inGameAddress") or "").strip() or "(no address)"
        print(f"  {record.get('id', '?'):<8} {name}")


def main(argv=None):
    args = parse_args(argv)
    records = load_dataset(args.dataset)
    regions = load_regions(args.regions)
    aliases = alias_map(regions)
    counts = coverage(records, aliases)
    print_table(counts)
    if not args.table_only:
        print_gaps(records, aliases)

    named_without_place = sum(
        1 for r in records if is_named(r) and not is_positioned(r)
    )
    print()
    print(f"Named but unpositioned: {named_without_place}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
