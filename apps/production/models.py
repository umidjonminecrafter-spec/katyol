from sqlalchemy import Column, String, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from core.base_model import BaseModel

class ProductionBatch(BaseModel):
    __tablename__ = "production_batches"

    batch_number = Column(String(50), unique=True, nullable=False)
    boiler_id = Column(String(36), ForeignKey("boilers.id"), nullable=False)
    target_quantity = Column(Integer, nullable=False)
    completed_quantity = Column(Integer, default=0)
    defect_quantity = Column(Integer, default=0)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    status = Column(String(30), default="PLANNED", nullable=False)

    boiler = relationship("Boiler", lazy="selectin")
