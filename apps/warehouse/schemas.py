from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class StockResponse(BaseModel):
    id: str
    warehouse_id: str
    warehouse_name: Optional[str] = None
    product_id: str
    product_code: Optional[str] = None
    product_name: Optional[str] = None
    quantity: float
    reserved_quantity: float
    available_quantity: float = 0.0
    avg_unit_cost: float
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class StockAdjustmentRequest(BaseModel):
    warehouse_id: str
    product_id: str
    quantity_delta: float
    notes: Optional[str] = None
