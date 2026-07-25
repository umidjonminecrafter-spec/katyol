from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from core.base_model import BaseModel

class Organization(BaseModel):
    __tablename__ = "organizations"

    name = Column(String(255), nullable=False)
    description = Column(String(500), nullable=True)

class Branch(BaseModel):
    __tablename__ = "branches"

    organization_id = Column(String(36), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    code = Column(String(50), nullable=False)
    address = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)

class User(BaseModel):
    __tablename__ = "users"

    username = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=True)
    role = Column(String(50), nullable=False, default="EMPLOYEE")
    position_id = Column(String(36), ForeignKey("positions.id"), nullable=True)
    department = Column(String(100), nullable=True)
    organization_name = Column(String(255), nullable=True)
    branch_name = Column(String(255), nullable=True)
    
    # Proper relations for multi-branch switching
    organization_id = Column(String(36), ForeignKey("organizations.id", ondelete="SET NULL"), nullable=True)
    branch_id = Column(String(36), ForeignKey("branches.id", ondelete="SET NULL"), nullable=True)

    salary_amount = Column(String(50), nullable=True)
    salary_type_id = Column(String(36), nullable=True)
    hire_date = Column(String(50), nullable=True)

    position = relationship("Position", back_populates="users", lazy="selectin")

class Position(BaseModel):
    __tablename__ = "positions"

    code = Column(String(50), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(String(500), nullable=True)
    permissions = Column(String(2000), nullable=True)

    users = relationship("User", back_populates="position")

class UserSession(BaseModel):
    __tablename__ = "user_sessions"

    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    refresh_token = Column(String(500), nullable=False, index=True)
    user_agent = Column(String(500), nullable=True)
    ip_address = Column(String(45), nullable=True)
    expires_at = Column(String(100), nullable=False)
