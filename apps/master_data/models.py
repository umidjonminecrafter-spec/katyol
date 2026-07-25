from sqlalchemy import Column, String, Text, Numeric
from core.base_model import BaseModel

class ProductCategory(BaseModel):
    __tablename__ = "product_categories"
    code = Column(String(50), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

class MaterialType(BaseModel):
    __tablename__ = "material_types"
    code = Column(String(50), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

class Unit(BaseModel):
    __tablename__ = "units"
    code = Column(String(50), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    symbol = Column(String(20), nullable=True)

class Supplier(BaseModel):
    __tablename__ = "suppliers"
    code = Column(String(50), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    contact_name = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    email = Column(String(255), nullable=True)
    address = Column(Text, nullable=True)

class Customer(BaseModel):
    __tablename__ = "customers"
    code = Column(String(50), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    contact_name = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    email = Column(String(255), nullable=True)
    address = Column(Text, nullable=True)

class Warehouse(BaseModel):
    __tablename__ = "warehouses"
    code = Column(String(50), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    location = Column(String(255), nullable=True)

class WarrantyType(BaseModel):
    __tablename__ = "warranty_types"
    code = Column(String(50), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    months = Column(Numeric(5, 0), default=12)

class CustomerType(BaseModel):
    __tablename__ = "customer_types"
    code = Column(String(50), unique=True, nullable=False)
    name = Column(String(255), nullable=False)

class ServiceType(BaseModel):
    __tablename__ = "service_types"
    code = Column(String(50), unique=True, nullable=False)
    name = Column(String(255), nullable=False)

class Priority(BaseModel):
    __tablename__ = "priorities"
    code = Column(String(50), unique=True, nullable=False)
    name = Column(String(255), nullable=False)

class OrderStatus(BaseModel):
    __tablename__ = "order_statuses"
    code = Column(String(50), unique=True, nullable=False)
    name = Column(String(255), nullable=False)

class ExpenseType(BaseModel):
    __tablename__ = "expense_types"
    code = Column(String(50), unique=True, nullable=False)
    name = Column(String(255), nullable=False)

class Company(BaseModel):
    __tablename__ = "company_profile"
    name = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=True)
    website = Column(String(255), nullable=True)
    address = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    currency = Column(String(20), default="USD")
    timezone = Column(String(100), default="Asia/Tashkent (UTC+5)")
    date_format = Column(String(50), default="YYYY-MM-DD")
