from datetime import datetime, timezone

from fastapi import APIRouter

from backend.app.config.settings import get_settings

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check() -> dict[str, str]:
    settings = get_settings()
    return {
        "status": "ok",
        "app": settings.app_name,
        "data_source": settings.data_source,
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }

