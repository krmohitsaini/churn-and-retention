from pydantic import BaseModel, Field
from typing import Optional


class CustomerDetail(BaseModel):
    customer: dict
    propensity: Optional[dict] = None
    interactions: list[dict] = Field(default_factory=list)
