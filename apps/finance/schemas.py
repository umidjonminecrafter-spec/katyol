from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import date, datetime

class TransactionCreate(BaseModel):
    transaction_number: str
    type: str
    expense_type_id: Optional[str] = None
    amount: float
    currency: str = "USD"
    reference_id: Optional[str] = None
    transaction_date: date
    notes: Optional[str] = None

class TransactionResponse(BaseModel):
    id: str
    transaction_number: str
    type: str
    expense_type_id: Optional[str] = None
    amount: float
    currency: str
    reference_id: Optional[str] = None
    transaction_date: date
    notes: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
