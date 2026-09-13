from fastapi import APIRouter, Depends, Query
from typing import Optional

from backend.app.data import get_repository
from backend.app.data.base_repository import BaseRepository
from backend.app.services.portfolio_service import PortfolioService

router = APIRouter(prefix="/portfolio", tags=["portfolio"])


def get_service(repository: BaseRepository = Depends(get_repository)) -> PortfolioService:
    return PortfolioService(repository)


def portfolio_filters(
    commodity_type: Optional[str] = Query(default=None),
    channel: Optional[str] = Query(default=None),
    sales_type: Optional[str] = Query(default=None),
    AMB_status: Optional[str] = Query(default=None),
    evergreen_status: Optional[str] = Query(default=None),
    surge_status: Optional[str] = Query(default=None),
    digital_status: Optional[str] = Query(default=None),
    dob_status: Optional[str] = Query(default=None),
) -> dict:
    return {
        "commodity_type": commodity_type,
        "channel": channel,
        "sales_type": sales_type,
        "AMB_status": AMB_status,
        "evergreen_status": evergreen_status,
        "surge_status": surge_status,
        "digital_status": digital_status,
        "dob_status": dob_status,
    }


@router.get("/summary")
def summary(
    filters: dict = Depends(portfolio_filters),
    service: PortfolioService = Depends(get_service),
) -> dict:
    return service.summary(filters)


@router.get("/segments")
def segments(service: PortfolioService = Depends(get_service)) -> dict:
    return service.segments()


@router.get("/timeseries")
def timeseries(service: PortfolioService = Depends(get_service)) -> list[dict]:
    return service.timeseries()
