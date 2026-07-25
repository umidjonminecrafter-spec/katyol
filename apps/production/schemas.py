from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import date, datetime

class ProductionBatchCreate(BaseModel):
    batch_number: str
    boiler_id: str
    target_quantity: int
    start_date: Optional[date] = None
    end_date: Optional[date] = None

class ProductionBatchUpdate(BaseModel):
    completed_quantity: Optional[int] = None
    defect_quantity: Optional[int] = None
    status: Optional[str] = None

class ProductionBatchResponse(BaseModel):
    id: str
    batch_number: str
    boiler_id: str
    boiler_name: Optional[str] = None
    target_quantity: int
    completed_quantity: int
    defect_quantity: int
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
