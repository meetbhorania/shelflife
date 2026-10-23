"""Finds charities near the café that accept the kinds of food on offer."""

import json
import math

from .paths import DATA_DIR

# Encode Hub, 41 Pitfield St, London — where the café in the demo is.
CAFE_LAT, CAFE_LON = 51.5287, -0.0838


def _miles_between(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 3958.8  # Earth radius in miles
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def find_nearby_charities(categories: list[str], max_miles: float = 3.0) -> dict:
    """Finds charities within `max_miles` of the café that accept at least one of the categories.

    Args:
        categories: Food categories on offer, e.g. ["bakery", "ready-meal"].
        max_miles: How far a charity can be from the café.

    Returns:
        A dict with `charities`, closest first. Each has the categories it will take
        and its collection slots.
    """
    with open(DATA_DIR / "charities.json") as f:
        charities = json.load(f)

    wanted = set(categories)
    matches = []
    for c in charities:
        takes = sorted(wanted & set(c["accepts"]))
        if not takes:
            continue
        miles = _miles_between(CAFE_LAT, CAFE_LON, c["lat"], c["lon"])
        if miles <= max_miles:
            matches.append(
                {
                    "id": c["id"],
                    "name": c["name"],
                    "miles": round(miles, 1),
                    "takes": takes,
                    "collection_slots": c["collection_slots"],
                }
            )

    matches.sort(key=lambda m: m["miles"])
    return {"charities": matches}
