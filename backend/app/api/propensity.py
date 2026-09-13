from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional

from backend.app.data import get_repository
from backend.app.data.base_repository import BaseRepository
from backend.app.services.propensity_service import PropensityService

router = APIRouter(prefix="/propensity", tags=["propensity"])


def get_service(repository: BaseRepository = Depends(get_repository)) -> PropensityService:
    return PropensityService(repository)


def propensity_filters(
    province: Optional[str] = Query(default=None),
    segment: Optional[str] = Query(default=None),
    product_type: Optional[str] = Query(default=None),
    risk_band: Optional[str] = Query(default=None),
    prediction_window_days: Optional[int] = Query(default=None),
) -> dict:
    return {
        "province": province,
        "segment": segment,
        "product_type": product_type,
        "risk_band": risk_band,
        "prediction_window_days": prediction_window_days,
    }


@router.get("/summary")
def summary(filters: dict = Depends(propensity_filters), service: PropensityService = Depends(get_service)) -> dict:
    return service.summary(filters)


@router.get("/customers")
def customers(filters: dict = Depends(propensity_filters), service: PropensityService = Depends(get_service)) -> list[dict]:
    return service.customers(filters)


@router.get("/customers/{customer_id}")
def customer(customer_id: str, service: PropensityService = Depends(get_service)) -> dict:
    row = service.customer(customer_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Customer score not found")
    return row


@router.get("/drivers")
def drivers(service: PropensityService = Depends(get_service)) -> list[dict]:
    return service.drivers()
