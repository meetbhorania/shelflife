"""ShelfLife: helps a café donate end-of-day surplus food to nearby charities.

coordinator (LlmAgent)
├── plan_pickup (SequentialAgent)
│   ├── stock_reader     → read_surplus_list        (saves: stock_summary)
│   └── charity_matcher  → find_nearby_charities    (saves: charity_options)
└── booking_agent        → book_collection          (only after the café says yes)
"""

import os

from google.adk.agents import LlmAgent, SequentialAgent

from . import prompts
from .tools import book_collection, find_nearby_charities, read_surplus_list

MODEL = os.getenv("SHELFLIFE_MODEL", "gemini-3.5-flash")

stock_reader = LlmAgent(
    name="stock_reader",
    model=MODEL,
    description="Reads the surplus list and removes food past its use-by date.",
    instruction=prompts.STOCK_READER,
    tools=[read_surplus_list],
    output_key="stock_summary",
)

charity_matcher = LlmAgent(
    name="charity_matcher",
    model=MODEL,
    description="Finds nearby charities that accept the food on offer.",
    instruction=prompts.CHARITY_MATCHER,
    tools=[find_nearby_charities],
    output_key="charity_options",
)

plan_pickup = SequentialAgent(
    name="plan_pickup",
    description="Checks today's surplus, then suggests charities that can collect it.",
    sub_agents=[stock_reader, charity_matcher],
)

booking_agent = LlmAgent(
    name="booking_agent",
    model=MODEL,
    description="Books a collection once the café has confirmed the charity, slot and items.",
    instruction=prompts.BOOKING_AGENT,
    tools=[book_collection],
)

root_agent = LlmAgent(
    name="shelflife",
    model=MODEL,
    description="Helps a café donate its leftover food to local charities.",
    instruction=prompts.COORDINATOR,
    sub_agents=[plan_pickup, booking_agent],
)
