from typing import Optional, List
from pydantic import BaseModel, ConfigDict

class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    phone: str
    password: str
    full_name: str
    organization_name: str
    branch_name: str
    currency: str

class UserCreate(BaseModel):
    phone: str
    password: str
    full_name: str
    role: str = "EMPLOYEE"
    position_id: Optional[str] = None
    department: Optional[str] = None
    salary_amount: Optional[str] = None
    salary_type_id: Optional[str] = None
    hire_date: Optional[str] = None

class UserInfo(BaseModel):
    id: str
    full_name: str
    role: str
    username: Optional[str] = None
    phone: Optional[str] = None
    department: Optional[str] = None
    organization_name: Optional[str] = None
    branch_name: Optional[str] = None
    organization_id: Optional[str] = None
    branch_id: Optional[str] = None
    salary_amount: Optional[str] = None
    salary_type_id: Optional[str] = None
    hire_date: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class TokenData(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserInfo

class LoginResponse(BaseModel):
    success: bool = True
    data: TokenData

class RefreshRequest(BaseModel):
    refresh_token: str

class RefreshResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserProfileResponse(BaseModel):
    user: UserInfo
    permissions: List[str]

class BranchCreate(BaseModel):
    name: str
    code: str
    address: Optional[str] = None
    phone: Optional[str] = None

class BranchResponse(BaseModel):
    id: str
    organization_id: str
    name: str
    code: str
    address: Optional[str] = None
    phone: Optional[str] = None
    status: str

    model_config = ConfigDict(from_attributes=True)

class PositionCreate(BaseModel):
    name: str
    description: Optional[str] = None
    permissions: Optional[str] = None

class PositionResponse(BaseModel):
    id: str
    code: str
    name: str
    description: Optional[str] = None
    permissions: Optional[str] = None
    status: str

    model_config = ConfigDict(from_attributes=True)
