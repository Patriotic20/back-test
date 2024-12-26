from sqlalchemy import UUID, Column, String, DateTime, Float, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum

from src.base.db import Base


class PaymentMethod(enum.Enum):
    cash = "Cash"
    card = "Card"
    online = "Online"


class StatusEnum(enum.Enum):
    selling = "selling"
    sold = "sold"
    payback = "payback"


class Sale(Base):
    __tablename__ = "sales"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    seller_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    quantity_sold = Column(Integer, nullable=False)
    sale_date = Column(DateTime, default=datetime.utcnow)
    payment_method = Column(Enum(PaymentMethod))  # e.g., Cash, Card, etc.
    discount = Column(Float, default=0.0)
    tax = Column(Float, default=0.0)
    status = Column(Enum(StatusEnum))
    random_numbers = Column(String)

    product = relationship("Product", back_populates="sales")
    seller = relationship("User", back_populates="sales")
