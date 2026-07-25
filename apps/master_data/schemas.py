from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class MasterDataCreate(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    contact_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    location: Optional[str] = None
    months: Optional[float] = None
    symbol: Optional[str] = None

class MasterDataUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    contact_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    location: Optional[str] = None
    months: Optional[float] = None
    symbol: Optional[str] = None
    status: Optional[str] = None

class MasterDataResponse(BaseModel):
    id: str
    code: str
    name: str
    description: Optional[str] = None
    contact_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    location: Optional[str] = None
    months: Optional[float] = None
    symbol: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    address: Optional[str] = None
    description: Optional[str] = None
    currency: Optional[str] = None
    timezone: Optional[str] = None
    date_format: Optional[str] = None

class CompanyResponse(BaseModel):
    id: str
    name: str
    phone: Optional[str] = None
    website: Optional[str] = None
    address: Optional[str] = None
    description: Optional[str] = None
    currency: str
    timezone: str
    date_format: str

    model_config = ConfigDict(from_attributes=True)
