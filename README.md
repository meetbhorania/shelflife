# ShelfLife

Small cafés throw away good food every evening because arranging a pickup takes too long.
ShelfLife is an agent that turns the café's end-of-day surplus list into a booked charity collection in a couple of messages.

Built at the GDG London AIDevCamp Agentic Hackathon with Google ADK.

## How it works

```
shelflife (coordinator)
├── plan_pickup (SequentialAgent)
│   ├── stock_reader     reads the surplus list, removes anything past its use-by date
│   └── charity_matcher  finds nearby charities that accept the food
└── booking_agent        books a collection, only after the café confirms
```

- Agents share results through session state (`stock_summary`, `charity_options`).
- `book_collection` refuses to book unless the café has confirmed, and checks the slot is real.
- Expired food is never offered to a charity.

## Run it

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example shelflife/.env      # then add your Gemini API key
adk web                             # open http://localhost:8000 and pick "shelflife"
```

Try: *"Closing up — what can we give away tonight?"* then *"Book Shoreditch Night Shelter at 17:30 for the wraps and soup."*

## Tests

```bash
pytest
```

## Data

`data/surplus_today.csv` and `data/charities.json` are sample data for the demo. Charities and contacts are made up.
