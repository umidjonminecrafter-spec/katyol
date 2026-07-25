from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class ProductCreate(BaseModel):
    code: str
    name: str
    category_id: str
    material_type_id: Optional[str] = None
    unit_id: str
    supplier_id: Optional[str] = None
    type: str  # 'FINISHED_GOOD', 'RAW_MATERIAL', 'SPARE_PART'
    min_stock_level: float = 0.0
    unit_price: float = Field(default=0.0, ge=0.0)
    currency: str = "USD"

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    category_id: Optional[str] = None
    material_type_id: Optional[str] = None
    unit_id: Optional[str] = None
    supplier_id: Optional[str] = None
    type: Optional[str] = None
    min_stock_level: Optional[float] = None
    unit_price: Optional[float] = None
    currency: Optional[str] = None
    status: Optional[str] = None

class ProductResponse(BaseModel):
    id: str
    code: str
    name: str
    category_id: str
    category_name: Optional[str] = None
    material_type_id: Optional[str] = None
    material_type_name: Optional[str] = None
    unit_id: str
    unit_name: Optional[str] = None
    supplier_id: Optional[str] = None
    supplier_name: Optional[str] = None
    type: str
    unit_price: float
    min_stock_level: float
    currency: str
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class RecipeItemSchema(BaseModel):
    material_product_id: str
    quantity: float
    waste_percentage: float = 0.0

class RecipeItemResponse(BaseModel):
    id: str
    recipe_id: str
    material_product_id: str
    material_name: Optional[str] = None
    quantity: float
    waste_percentage: float

    model_config = ConfigDict(from_attributes=True)

class RecipeCreate(BaseModel):
    recipe_number: str
    product_id: str
    version: str = "v1.0"
    estimated_cost: float = 0.0
    items: List[RecipeItemSchema] = []

class RecipeResponse(BaseModel):
    id: str
    recipe_number: str
    product_id: str
    version: str
    estimated_cost: float
    status: str
    items: List[RecipeItemResponse] = []

    model_config = ConfigDict(from_attributes=True)

class BoilerCreate(BaseModel):
    model_code: str
    name: str
    capacity_kw: float
    fuel_type: str  # 'GAS', 'COAL', 'ELECTRIC', 'DUAL'
    efficiency_percent: Optional[float] = None
    base_price: float
    recipe_id: Optional[str] = None
    warranty_type_id: Optional[str] = None

class BoilerResponse(BaseModel):
    id: str
    model_code: str
    name: str
    capacity_kw: float
    fuel_type: str
    efficiency_percent: Optional[float] = None
    base_price: float
    recipe_id: Optional[str] = None
    warranty_type_id: Optional[str] = None
    status: str

    model_config = ConfigDict(from_attributes=True)
