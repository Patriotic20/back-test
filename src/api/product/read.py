from fastapi import APIRouter, Depends
from typing import List
from src.schemas.product import ProductResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.base.db import get_db
from src.models.product import Product

router = APIRouter()


@router.get("/products", response_model=List[ProductResponse])
async def list_products(barcode: str, db: AsyncSession = Depends(get_db)):
    product = await db.execute(select(Product).where(Product.barcode == barcode))
    return product.scalars().first()
