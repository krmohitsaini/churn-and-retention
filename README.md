# Churn and Retention

Customer retention and churn analytics app for NRG Canada.

The first version runs locally with CSV-backed sample data. The architecture is intentionally split into frontend pages, frontend API wrappers, backend routes, services, KPI modules, and data repositories so the app can later move from CSV files to Databricks tables without rewriting the UI.

## Where to Put Your CSV Files

Place dummy CSV files in:

```text
data/sample/
```

Recommended starting files:

- `customers.csv`
- `churn_events.csv`
- `propensity_scores.csv`
- `customer_interactions.csv`
- `offers.csv`

If you also have schema notes, place them in:

```text
data/sample/SCHEMA.md
```

Raw client extracts can go in `data/raw/`. Cleaned or transformed files can go in `data/processed/`.

## Local Development

Backend:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.app.main:app --reload --port 5050
```

Frontend:

```bash
cd frontend
npm install
VITE_API_BASE_URL=http://localhost:5050 npm run dev
```

Open the frontend URL shown by Vite.

## Architecture

- `frontend/src/pages/`: one file per app page
- `frontend/src/api/`: one API wrapper per page/domain
- `backend/app/api/`: FastAPI route files
- `backend/app/services/`: business orchestration
- `backend/app/kpis/`: KPI calculations and definitions
- `backend/app/data/`: CSV and future Databricks repositories
- `backend/app/schemas/`: API response/request schemas

## Data Source

The app defaults to CSV mode.

Environment variables:

- `APP_DATA_SOURCE=csv`
- `APP_SAMPLE_DATA_DIR=data/sample`

Later, `APP_DATA_SOURCE=databricks` can be used once the Databricks repository is implemented.

## Caching

The backend caches expensive Portfolio and Churn aggregate responses using the data source version and active filters as the cache key. In CSV mode, the source version includes the raw CSV file modification time, so replacing the CSV naturally invalidates the cache after the backend restarts or sees the new timestamp.

The frontend also keeps a small in-memory GET cache during the browser session so switching between pages does not refetch identical dashboard payloads.
