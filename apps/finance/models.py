from sqlalchemy import Column, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship
from core.base_model import BaseModel

class FinancialTransaction(BaseModel):
    __tablename__ = "financial_transactions"

    transaction_number = Column(String(50), unique=True, nullable=False)
    type = Column(String(20), nullable=False)  # 'INCOME', 'EXPENSE'
    expense_type_id = Column(String(36), ForeignKey("expense_types.id"), nullable=True)
    amount = Column(Numeric(15, 2), nullable=False)
    currency = Column(String(10), default="USD")
    reference_id = Column(String(100), nullable=True)
    transaction_date = Column(Date, nullable=False)
    notes = Column(String(500), nullable=True)

    expense_type = relationship("ExpenseType", lazy="selectin")
