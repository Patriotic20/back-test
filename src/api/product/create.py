from fastapi import APIRouter, Depends
from src.schemas.product import ProductResponse, ProductCreate
from sqlalchemy.ext.asyncio import AsyncSession
from src.base.db import get_db
from sqlalchemy import select
from src.models.product import Product

router = APIRouter()

# dependencies=[Depends(require_role("Admin"))]


@router.post("/products", response_model=ProductResponse)
async def create_product(
    product: ProductCreate,
    db: AsyncSession = Depends(get_db),
):
    action = await db.execute(select(Product).where(Product.barcode == product.barcode))
    action = action.scalars().first()

    if action:
        action.stock_quantity += 1
        await db.commit()
        return action
    else:
        new_product = Product(**product.model_dump())
        db.add(new_product)
        await db.commit()
        await db.refresh(new_product)
        return new_product
