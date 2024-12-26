from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.base.db import get_db
from sqlalchemy import select
from src.models.sale import Sale


router = APIRouter()


@router.delete("/")
async def delete_sale(db: AsyncSession = Depends(get_db)):
    sale = await db.execute(select(Sale))
    sale = sale.scalars().all()

    for sale_item in sale:
        await db.delete(sale_item)
    await db.commit()
    return "Delete"
