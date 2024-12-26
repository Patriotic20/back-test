from src.models.sale import PaymentMethod
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import uuid


class SaleBase(BaseModel):
    product_id: uuid.UUID
    seller_id: uuid.UUID
    quantity_sold: int
    payment_method: PaymentMethod
    discount: Optional[float] = 0.0
    tax: Optional[float] = 0.0


class SaleCreate(SaleBase):
    pass


class SaleResponse(SaleBase):
    id: uuid.UUID
    sale_date: datetime

    class Config:
        from_attributes = True
