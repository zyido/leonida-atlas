# Leonida Atlas — dataset reports

Processing scripts and audit reports for the open Leonida place dataset used by
the interactive map. The point of this repo is the **audit**: how many records
exist, how many actually have coordinates, how many have names, and where the
gaps are.

## What's here

| Path | What it is |
| --- | --- |
| `data/leonida.json` | The dataset snapshot: 3,431 landmark records |
| `data/regions.json` | Six regions, their alias lists and the published totals |
| `data/SOURCE.md` | Upstream link, pinned revision, checksums and licence |
| `scripts/leonida.py` | Shared field definitions: positioned, named, region |
| `scripts/audit.py` | Coverage table, plus every record missing a position or a region |
| `scripts/region_totals.py` | Per-region totals; fails when they drift from the published ones |
| `scripts/export_geojson.py` | Writes the positioned records as a FeatureCollection |

## Links

- Interactive map — https://zonepedia.com/gta-6/map
- Locations index — https://zonepedia.com/gta-6/locations
- About this project and its sources — https://zonepedia.com/about

## Disclaimer

Unofficial, fan-made dataset project. Not affiliated with any game publisher.
All place names and any game assets belong to their respective owners.
