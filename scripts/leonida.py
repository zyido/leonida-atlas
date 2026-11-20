"""Shared helpers for the Leonida Atlas audit scripts.

The field definitions in ``data/regions.json`` are the authority here, not this
module: a record is *positioned* when it carries a finite in-game coordinate
pair, *named* when its in-game address is non-empty and contains no question
mark, and its *region* is the final address label matched case-insensitively
against the region aliases. Regions are never inferred from coordinates.

Everything is standard library; the scripts run on any Python 3.8+.
"""

import json
import math


def load_dataset(path):
    """Return the landmark records from a catalogue file.

    Accepts either the upstream catalogue (a dict with a ``landmarks`` array)
    or a bare array, so a trimmed export works the same way.
    """
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    if isinstance(data, dict):
        return data.get("landmarks") or []
    return data


def load_regions(path):
    """Return the parsed regions file (totals, definitions and aliases)."""
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def is_positioned(record):
    coords = record.get("inGameCoordinates")
    if not isinstance(coords, list) or len(coords) != 2:
        return False
    for value in coords:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            return False
        if not math.isfinite(value):
            return False
    return True


def is_named(record):
    address = (record.get("inGameAddress") or "").strip()
    return bool(address) and "?" not in address


def source_label(record):
    """The final comma-separated part of the in-game address."""
    return (record.get("inGameAddress") or "").split(",")[-1].strip()


def alias_map(regions):
    """Map a casefolded source label to a region slug."""
    aliases = {}
    for region in regions.get("regions", []):
        for label in region.get("sourceLabels", []):
            aliases.setdefault(label.strip().casefold(), region["slug"])
    return aliases


def region_of(record, aliases):
    """Region slug for a record, or None when its label has no mapping."""
    return aliases.get(source_label(record).casefold())


def coverage(records, aliases):
    """Counts used by the README table and by the audit script."""
    total = len(records)
    positioned = sum(1 for r in records if is_positioned(r))
    named = sum(1 for r in records if is_named(r))
    assigned = sum(1 for r in records if region_of(r, aliases))
    return {
        "total": total,
        "positioned": positioned,
        "named": named,
        "unpositioned": total - positioned,
        "unassigned": total - assigned,
    }
