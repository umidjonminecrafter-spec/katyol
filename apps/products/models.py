from sqlalchemy import Column, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from core.base_model import BaseModel

class Product(BaseModel):
    __tablename__ = "products"

    code = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    category_id = Column(String(36), ForeignKey("product_categories.id"), nullable=False)
    material_type_id = Column(String(36), ForeignKey("material_types.id"), nullable=True)
    unit_id = Column(String(36), ForeignKey("units.id"), nullable=False)
    supplier_id = Column(String(36), ForeignKey("suppliers.id"), nullable=True)
    
    type = Column(String(50), nullable=False)  # 'FINISHED_GOOD', 'RAW_MATERIAL', 'SPARE_PART'
    min_stock_level = Column(Numeric(15, 3), default=0.000)
    unit_price = Column(Numeric(15, 2), default=0.00)
    currency = Column(String(10), default="USD")

    category = relationship("ProductCategory", lazy="selectin")
    material_type = relationship("MaterialType", lazy="selectin")
    unit = relationship("Unit", lazy="selectin")
    supplier = relationship("Supplier", lazy="selectin")

class Recipe(BaseModel):
    __tablename__ = "recipes"

    recipe_number = Column(String(50), unique=True, nullable=False)
    product_id = Column(String(36), ForeignKey("products.id"), nullable=False)
    version = Column(String(20), default="v1.0")
    estimated_cost = Column(Numeric(15, 2), default=0.00)

    product = relationship("Product", lazy="selectin")
    items = relationship("RecipeItem", back_populates="recipe", cascade="all, delete-orphan", lazy="selectin")

class RecipeItem(BaseModel):
    __tablename__ = "recipe_items"

    recipe_id = Column(String(36), ForeignKey("recipes.id", ondelete="CASCADE"), nullable=False)
    material_product_id = Column(String(36), ForeignKey("products.id"), nullable=False)
    quantity = Column(Numeric(15, 3), nullable=False)
    waste_percentage = Column(Numeric(5, 2), default=0.00)

    recipe = relationship("Recipe", back_populates="items")
    material_product = relationship("Product", lazy="selectin")

class Boiler(BaseModel):
    __tablename__ = "boilers"

    model_code = Column(String(100), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    capacity_kw = Column(Numeric(10, 2), nullable=False)
    fuel_type = Column(String(50), nullable=False)  # 'GAS', 'COAL', 'ELECTRIC', 'DUAL'
    efficiency_percent = Column(Numeric(5, 2), nullable=True)
    base_price = Column(Numeric(15, 2), nullable=False)
    recipe_id = Column(String(36), ForeignKey("recipes.id"), nullable=True)
    warranty_type_id = Column(String(36), ForeignKey("warranty_types.id"), nullable=True)

    recipe = relationship("Recipe", lazy="selectin")
    warranty_type = relationship("WarrantyType", lazy="selectin")
