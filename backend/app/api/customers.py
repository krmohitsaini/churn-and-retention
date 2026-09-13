from fastapi import APIRouter, Depends, HTTPException

from backend.app.data import get_repository
from backend.app.data.base_repository import BaseRepository
from backend.app.services.customer_service import CustomerService

router = APIRouter(prefix="/customers", tags=["customers"])


def get_service(repository: BaseRepository = Depends(get_repository)) -> CustomerService:
    return CustomerService(repository)


@router.get("/{customer_id}")
def detail(customer_id: str, service: CustomerService = Depends(get_service)) -> dict:
    row = service.detail(customer_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return row

