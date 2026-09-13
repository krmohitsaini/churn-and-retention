from fastapi import APIRouter, Depends
from fastapi.responses import Response

from backend.app.data import get_repository
from backend.app.data.base_repository import BaseRepository
from backend.app.services.export_service import ExportService
from backend.app.services.propensity_service import PropensityService

router = APIRouter(prefix="/exports", tags=["exports"])


@router.post("/propensity")
def export_propensity(repository: BaseRepository = Depends(get_repository)) -> Response:
    customers = PropensityService(repository).customers({})
    csv_text = ExportService().propensity_csv(customers)
    return Response(
        content=csv_text,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=propensity_customers.csv"},
    )

