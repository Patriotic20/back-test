from fastapi import APIRouter , Depends
from typing import List
from src.schemas.product import ProductResponse , ProductCreate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.settings.db import get_db
from src.models.product import Product
import uuid


# response_model=ProductResponse
router = APIRouter()

@router.put("/products/{product_id}")
async def update_product(
    barcode : str,
    name : str | None = None ,
    stock_quantity : int |None = None,
    price : float | None = None,
    category : str | None = None, 
    db : AsyncSession = Depends(get_db)):

    product = await db.execute(select(Product).where(Product.barcode == barcode))
    product = product.scalars().first()

    if name: 
        product.name = name
    if stock_quantity:
        product.stock_quantity = stock_quantity
    if price:
        product.price = price
    if category:
        product.category = category

    await db.commit()
    await db.refresh(product)
    return product

