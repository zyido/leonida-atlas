#!/usr/bin/env python3
"""Export the positioned records as a GeoJSON FeatureCollection.

    python3 scripts/export_geojson.py data/leonida.json out.geojson

The coordinates are **in-game map units, not latitude and longitude**. They are
a community reconstruction placed on the game's own map plane, so the output is
a valid FeatureCollection that is not geographically positioned — render it on
a custom projection, not on top of an Earth basemap.

Records with no position are skipped by default; pass --include-unpositioned to
emit them with a null geometry so nothing silently disappears.
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from leonida import (  # noqa: E402
    alias_map, is_positioned, load_dataset, load_regions, region_of, source_label,
)

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_REGIONS = os.path.join(HERE, os.pardir, "data", "regions.json")


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("dataset", help="path to data/leonida.json")
    parser.add_argument("output", help="path to write, e.g. out.geojson")
    parser.add_argument(
        "--regions",
        default=DEFAULT_REGIONS,
        help="path to data/regions.json (default: %(default)s)",
    )
    parser.add_argument(
        "--include-unpositioned",
        action="store_true",
        help="emit records without coordinates as features with null geometry",
    )
    return parser.parse_args(argv)


def feature(record, aliases):
    props = {
        "id": record.get("id"),
        "label": source_label(record) or None,
        "address": (record.get("inGameAddress") or "").strip() or None,
        "region": region_of(record, aliases),
        "tags": record.get("tags") or [],
        "confidence": record.get("confidence"),
    }
    geometry = None
    if is_positioned(record):
        x, y = record["inGameCoordinates"]
        geometry = {"type": "Point", "coordinates": [x, y]}
    return {"type": "Feature", "properties": props, "geometry": geometry}


def main(argv=None):
    args = parse_args(argv)
    records = load_dataset(args.dataset)
    regions = load_regions(args.regions)
    aliases = alias_map(regions)

    kept = [
        record for record in records
        if args.include_unpositioned or is_positioned(record)
    ]
    collection = {
        "type": "FeatureCollection",
        "name": "leonida-landmarks",
        "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:EPSG::0"}},
        "note": (
            "In-game map units, not latitude/longitude. Community reconstruction; "
            "positions are approximate."
        ),
        "features": [feature(record, aliases) for record in kept],
    }

    with open(args.output, "w", encoding="utf-8") as fh:
        json.dump(collection, fh, ensure_ascii=False, separators=(",", ":"))
        fh.write("\n")

    skipped = len(records) - len(kept)
    print(f"Wrote {len(kept)} features to {args.output} ({skipped} skipped)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
