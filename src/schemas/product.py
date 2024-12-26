from pydantic import BaseModel
import uuid
from datetime import datetime


class ProductBase(BaseModel):
    name: str
    barcode: str
    stock_quantity: int
    price: float
    category: str


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True
