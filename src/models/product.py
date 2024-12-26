from sqlalchemy import UUID, Column, String, DateTime, Float, Integer
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from src.base.db import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    barcode = Column(String, unique=True, nullable=False)
    stock_quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    sales = relationship("Sale", back_populates="product")
