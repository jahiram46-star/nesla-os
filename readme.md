# NESLA AI — Phase 0 Foundation

Starter FastAPI project scaffold for NESLA AI using SQLite (local development).

## Structure

- `app/`
  - `api/` - API route modules
  - `core/` - configuration and settings
  - `db/` - database setup and models
  - `modules/` - app feature modules
- `tests/` - test cases

## Run (development)

1. Create a virtual environment and activate it (optional but recommended):

```bash
python -m venv .venv
source .venv/Scripts/activate  # Windows PowerShell
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app (you can use the exact command below):

```bash
python -m uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000 and you should see:

```
{"name": "NESLA AI", "status": "running"}
```

## Tests

Run tests with `pytest`:

```bash
pytest -q
```

