"""Books a collection with a charity — only once the café has said yes."""

import json
from datetime import datetime

from google.adk.tools import ToolContext

from .paths import DATA_DIR


def book_collection(
    charity_id: str,
    slot: str,
    items: list[str],
    confirmed_by_cafe: bool,
    tool_context: ToolContext,
) -> dict:
    """Books a collection slot with a charity.

    Args:
        charity_id: The charity's id, e.g. "c2".
        slot: One of the charity's collection slots, e.g. "17:30".
        items: Names of the items the charity will collect.
        confirmed_by_cafe: True only if the café has clearly said yes to this exact booking.

    Returns:
        A dict with `status`: "booked", "needs_confirmation" or "error".
    """
    if not confirmed_by_cafe:
        return {
            "status": "needs_confirmation",
            "message": "Ask the café to confirm the charity, slot and items before booking.",
        }

    with open(DATA_DIR / "charities.json") as f:
        charities = {c["id"]: c for c in json.load(f)}
    charity = charities.get(charity_id)
    if charity is None:
        return {"status": "error", "message": f"No charity with id {charity_id}."}
    if slot not in charity["collection_slots"]:
        return {
            "status": "error",
            "message": f"{charity['name']} collects at {', '.join(charity['collection_slots'])}, not {slot}.",
        }

    booking = {
        "charity": charity["name"],
        "contact": charity["contact"],
        "slot": slot,
        "items": items,
        "booked_at": datetime.now().isoformat(timespec="seconds"),
    }
    path = DATA_DIR / "bookings.json"
    bookings = json.loads(path.read_text()) if path.exists() else []
    bookings.append(booking)
    path.write_text(json.dumps(bookings, indent=2))

    tool_context.state["last_booking"] = booking
    return {"status": "booked", "booking": booking}
