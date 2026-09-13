from fastapi import APIRouter

from backend.app.config.settings import get_settings
from backend.app.services.app_cache import stats as cache_stats

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/kpis")
def kpis() -> list[dict[str, str]]:
    return [
        {
            "name": "Active customers",
            "definition": "Customers where current_status equals Active.",
            "module": "backend/app/kpis/portfolio_kpis.py",
        },
        {
            "name": "Gross churn rate",
            "definition": "Churned customers divided by starting customer count.",
            "module": "backend/app/kpis/churn_kpis.py",
        },
        {
            "name": "Revenue at risk",
            "definition": "Estimated annual value multiplied by churn probability.",
            "module": "backend/app/kpis/revenue_kpis.py",
        },
        {
            "name": "Retention rate",
            "definition": "One minus churned customers divided by total known customers.",
            "module": "backend/app/kpis/retention_kpis.py",
        },
    ]


@router.get("/apis")
def apis() -> list[dict[str, str]]:
    return [
        {"method": "GET", "path": "/api/v1/health", "description": "Backend health and data source status."},
        {"method": "GET", "path": "/api/v1/portfolio/summary", "description": "Portfolio KPIs and segmentation charts."},
        {"method": "GET", "path": "/api/v1/churn/summary", "description": "Churn KPIs, trends, and segment cuts."},
        {"method": "GET", "path": "/api/v1/propensity/summary", "description": "Customer-level churn risk and drivers."},
        {"method": "POST", "path": "/api/v1/exports/propensity", "description": "CSV export for propensity customers."},
    ]


@router.get("/data-status")
def data_status() -> dict[str, str]:
    settings = get_settings()
    return {
        "data_source": settings.data_source,
        "sample_data_dir": str(settings.sample_data_dir),
        "raw_data_file": str(settings.raw_data_file),
        "cache_entries": str(cache_stats()["entries"]),
        "status": "ready",
    }
