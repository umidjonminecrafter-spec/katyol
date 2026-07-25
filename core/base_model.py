import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Boolean
from core.database import Base

def generate_uuid() -> str:
    return str(uuid.uuid4())

class BaseModel(Base):
    __abstract__ = True

    id = Column(String(36), primary_key=True, default=generate_uuid)
    status = Column(String(20), nullable=False, default="ACTIVE")
    is_active = Column(Boolean, nullable=False, default=True)

    organization_id = Column(String(36), nullable=True)
    branch_id = Column(String(36), nullable=True)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    created_by_id = Column(String(36), nullable=True)
    updated_by_id = Column(String(36), nullable=True)
