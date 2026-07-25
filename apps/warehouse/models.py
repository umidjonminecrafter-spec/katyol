from sqlalchemy import Column, String, Numeric, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from core.base_model import BaseModel

class WarehouseStock(BaseModel):
    __tablename__ = "warehouse_stock"
    __table_args__ = (UniqueConstraint("warehouse_id", "product_id", name="uix_warehouse_product"),)

    warehouse_id = Column(String(36), ForeignKey("warehouses.id"), nullable=False)
    product_id = Column(String(36), ForeignKey("products.id"), nullable=False)
    quantity = Column(Numeric(15, 3), nullable=False, default=0.000)
    reserved_quantity = Column(Numeric(15, 3), default=0.000)
    avg_unit_cost = Column(Numeric(15, 2), default=0.00)

    warehouse = relationship("Warehouse", lazy="selectin")
    product = relationship("Product", lazy="selectin")

class StockMovement(BaseModel):
    __tablename__ = "stock_movements"

    movement_type = Column(String(50), nullable=False)
    product_id = Column(String(36), ForeignKey("products.id"), nullable=False)
    warehouse_id = Column(String(36), ForeignKey("warehouses.id"), nullable=False)
    quantity = Column(Numeric(15, 3), nullable=False)
    reference_id = Column(String(100), nullable=True)
    notes = Column(String(255), nullable=True)

    product = relationship("Product", lazy="selectin")
    warehouse = relationship("Warehouse", lazy="selectin")
