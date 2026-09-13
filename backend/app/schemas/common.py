from pydantic import BaseModel
from typing import Optional, Union


class ChartPoint(BaseModel):
    name: str
    value: Union[int, float]


class MetricCard(BaseModel):
    label: str
    value: Union[int, float, str]
    helper: Optional[str] = None
