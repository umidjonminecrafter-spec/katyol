from sqlalchemy import Column, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from core.base_model import BaseModel

class Sale(BaseModel):
    __tablename__ = "sales"

    invoice_number = Column(String(50), unique=True, nullable=False)
    customer_id = Column(String(36), ForeignKey("customers.id"), nullable=False)
    boiler_id = Column(String(36), ForeignKey("boilers.id"), nullable=True)
    product_id = Column(String(36), ForeignKey("products.id"), nullable=True)
    quantity = Column(Numeric(15, 3), nullable=False)
    unit_price = Column(Numeric(15, 2), nullable=False)
    subtotal = Column(Numeric(15, 2), nullable=False)
    discount_amount = Column(Numeric(15, 2), default=0.00)
    tax_amount = Column(Numeric(15, 2), default=0.00)
    total_amount = Column(Numeric(15, 2), nullable=False)
    exchange_rate_at_creation = Column(Numeric(10, 4), default=1.0000)

    payment_status = Column(String(20), default="UNPAID")
    delivery_status = Column(String(20), default="PENDING")

    customer = relationship("Customer", lazy="selectin")
    boiler = relationship("Boiler", lazy="selectin")
    product = relationship("Product", lazy="selectin")
