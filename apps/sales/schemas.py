from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class SaleCreate(BaseModel):
    invoice_number: str
    customer_id: str
    boiler_id: Optional[str] = None
    product_id: Optional[str] = None
    quantity: float
    unit_price: float
    discount_amount: float = 0.0
    tax_amount: float = 0.0
    exchange_rate_at_creation: float = 1.0

class SaleUpdateStatus(BaseModel):
    payment_status: Optional[str] = None
    delivery_status: Optional[str] = None

class SaleResponse(BaseModel):
    id: str
    invoice_number: str
    customer_id: str
    customer_name: Optional[str] = None
    boiler_id: Optional[str] = None
    product_id: Optional[str] = None
    quantity: float
    unit_price: float
    subtotal: float
    discount_amount: float
    tax_amount: float
    total_amount: float
    exchange_rate_at_creation: float
    payment_status: str
    delivery_status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
