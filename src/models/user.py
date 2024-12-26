from sqlalchemy import Column, String, UUID, DateTime, Enum
from src.base.db import Base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum


class UserRole(enum.Enum):
    manager = "manager"
    seller = "seller"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False, unique=True)
    role = Column(Enum(UserRole), nullable=False)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    sales = relationship("Sale", back_populates="seller")
