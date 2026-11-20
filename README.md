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

## Current dataset state

| Metric | Count |
| --- | --- |
| Records in dataset | 3,431 |
| Records with coordinates | 3,340 |
| Records with a name | 948 |
| Records with no location | 91 |
| Records with no region | 755 |

Two things worth flagging before you build on this:

- **91 records have no coordinates at all.** They exist in the source but cannot
  be placed on a map. We keep them in the dataset and exclude them from map
  rendering rather than deleting them.
- **755 records have no region assigned.** Region totals therefore are a floor,
  not a ceiling. If you aggregate by region you will lose those rows.

And the reverse: only 948 of 3,431 records carry a name, so any name-based
search covers roughly a quarter of the dataset. Most places are known by
position, not by label.

## Source and licence

Upstream dataset is published under CC BY 4.0. Attribution is required if you
redistribute. Source URL and the exact snapshot date are recorded in
`data/SOURCE.md` — check that file before reporting any number, because the
upstream set is versioned and counts move between releases.

## Scripts

```bash
python3 scripts/audit.py data/leonida.json     # reproduce the table above
python3 scripts/region_totals.py data/leonida.json
python3 scripts/export_geojson.py data/leonida.json out.geojson
```

`audit.py` prints the coverage table and lists every record missing a
coordinate or a region, so the gaps are reproducible rather than asserted.

`export_geojson.py` writes **in-game map units, not latitude and longitude** —
the output is a valid FeatureCollection that is not geographically positioned,
so render it on a custom projection rather than over an Earth basemap.

## Reporting

Issues are welcome for records that are clearly wrong (wrong region, duplicate
place, mislabelled type). Please include the record ID — not a screenshot —
so it can be checked against the source.

## Links

- Interactive map — https://zonepedia.com/gta-6/map
- Locations index — https://zonepedia.com/gta-6/locations
- About this project and its sources — https://zonepedia.com/about

## Disclaimer

Unofficial, fan-made dataset project. Not affiliated with any game publisher.
All place names and any game assets belong to their respective owners.
