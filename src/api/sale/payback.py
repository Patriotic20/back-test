from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.settings.db import get_db
from src.models import Sale , Product
from src.models.sale import StatusEnum
from src.other.errorrs import handle_exceptions
from src.other.dependies import require_role , get_current_user


router = APIRouter()

@router.post("/payback" , dependencies=[Depends(require_role("manger"))])
async def return_product(
    barcode : str,
    check_code : str,
    db: AsyncSession = Depends(get_db),
    current_user : dict = Depends(get_current_user),
    ):


    product = await db.execute(select(Product).where(Product.barcode == barcode))
    product = product.scalars().first()

    sale = await db.execute(
        select(Sale)
        .where(Sale.product_id == product.id and Sale.seller_id == current_user.get("user_id") and Sale.random_numbers == check_code))
    sale = sale.scalars().first()

    if  sale:
        product.stock_quantity += sale.quantity_sold
        sale.status = StatusEnum.payback


    await db.commit()
    await db.refresh(sale)
    return sale    


