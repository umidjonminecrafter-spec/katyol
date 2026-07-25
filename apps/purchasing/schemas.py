from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from datetime import date, datetime

class PurchaseItemCreate(BaseModel):
    product_id: str
    quantity: float = Field(..., gt=0)
    unit_price: float = Field(..., ge=0)

class PurchaseItemResponse(BaseModel):
    id: str
    product_id: str
    product_code: Optional[str] = None
    product_name: Optional[str] = None
    quantity: float
    unit_price: float
    total_price: float

    model_config = ConfigDict(from_attributes=True)

class PurchaseCreate(BaseModel):
    purchase_number: str
    supplier_id: str
    warehouse_id: str
    invoice_number: Optional[str] = None
    order_date: date
    tax_amount: float = 0.0
    exchange_rate_at_creation: float = 1.0
    items: List[PurchaseItemCreate]

class PurchaseUpdateStatus(BaseModel):
    status: str  # 'APPROVED', 'RECEIVED', 'CANCELLED'

class PurchaseResponse(BaseModel):
    id: str
    purchase_number: str
    supplier_id: str
    supplier_name: Optional[str] = None
    warehouse_id: str
    warehouse_name: Optional[str] = None
    invoice_number: Optional[str] = None
    order_date: date
    subtotal: float
    tax_amount: float
    total_amount: float
    exchange_rate_at_creation: float
    status: str
    created_at: datetime
    items: List[PurchaseItemResponse] = []

    model_config = ConfigDict(from_attributes=True)
