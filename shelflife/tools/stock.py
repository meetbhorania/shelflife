"""Reads the café's end-of-day surplus list and removes anything that isn't safe to give away."""

import csv
from datetime import date

from google.adk.tools import ToolContext

from .paths import DATA_DIR


def read_surplus_list(tool_context: ToolContext, today: str = "") -> dict:
    """Reads today's surplus list and splits it into food that can be donated and food that can't.

    Args:
        today: The date to check use-by dates against, as YYYY-MM-DD. Leave empty for today.

    Returns:
        A dict with `safe` items (still in date), `removed` items (past use-by, with a reason)
        and the food `categories` that are available.
    """
    check_date = date.fromisoformat(today) if today else date.today()
    safe, removed = [], []

    with open(DATA_DIR / "surplus_today.csv", newline="") as f:
        for row in csv.DictReader(f):
            use_by = date.fromisoformat(row["use_by"])
            item = {
                "item": row["item"],
                "quantity": int(row["quantity"]),
                "unit": row["unit"],
                "category": row["category"],
                "use_by": row["use_by"],
            }
            if use_by < check_date:
                removed.append({**item, "reason": f"use-by date {row['use_by']} has passed"})
            else:
                safe.append(item)

    categories = sorted({i["category"] for i in safe})
    tool_context.state["safe_items"] = safe
    tool_context.state["categories"] = categories
    return {"safe": safe, "removed": removed, "categories": categories}
