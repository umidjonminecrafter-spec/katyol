from sqlalchemy import Column, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship
from core.base_model import BaseModel

class Purchase(BaseModel):
    __tablename__ = "purchases"

    purchase_number = Column(String(50), unique=True, nullable=False)
    supplier_id = Column(String(36), ForeignKey("suppliers.id"), nullable=False)
    warehouse_id = Column(String(36), ForeignKey("warehouses.id"), nullable=False)
    invoice_number = Column(String(100), nullable=True)
    order_date = Column(Date, nullable=False)
    subtotal = Column(Numeric(15, 2), nullable=False, default=0.00)
    tax_amount = Column(Numeric(15, 2), default=0.00)
    total_amount = Column(Numeric(15, 2), nullable=False, default=0.00)
    exchange_rate_at_creation = Column(Numeric(10, 4), default=1.0000)
    status = Column(String(20), default="DRAFT", nullable=False)

    supplier = relationship("Supplier", lazy="selectin")
    warehouse = relationship("Warehouse", lazy="selectin")
    items = relationship("PurchaseItem", back_populates="purchase", cascade="all, delete-orphan", lazy="selectin")

class PurchaseItem(BaseModel):
    __tablename__ = "purchase_items"

    purchase_id = Column(String(36), ForeignKey("purchases.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(String(36), ForeignKey("products.id"), nullable=False)
    quantity = Column(Numeric(15, 3), nullable=False)
    unit_price = Column(Numeric(15, 2), nullable=False)
    total_price = Column(Numeric(15, 2), nullable=False)

    purchase = relationship("Purchase", back_populates="items")
    product = relationship("Product", lazy="selectin")
