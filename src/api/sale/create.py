from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.settings.db import get_db
from src.models import Product, Sale , User
from src.other.dependies import require_role, get_current_user
from src.other.errorrs import handle_exceptions
from src.schemas.sale import SaleResponse 
from src.models.sale import StatusEnum

router = APIRouter()

@router.post("/", dependencies=[Depends(require_role("seller"))])
@handle_exceptions
async def create_sale(
    barcode: str,
    quantity_sold: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # Fetch the product
    product_query = await db.execute(select(Product).where(Product.barcode == barcode))
    product = product_query.scalars().first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product with the given barcode not found."
        )

    # Check stock availability
    if quantity_sold > product.stock_quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not enough stock available."
        )

    # Check if a sale already exists for this product and seller
    sale_query = await db.execute(
        select(Sale).where(
            Sale.product_id == product.id,
            Sale.seller_id == current_user.get("user_id"),
            Sale.status == StatusEnum.selling
        )
    )
    sale = sale_query.scalars().first()

    # Deduct stock
    product.stock_quantity -= quantity_sold

    if sale:
        sale.quantity_sold += 1
        await db.commit()
        await db.refresh(sale)
        return sale
    else:
        # Create a new sale
        new_sale = Sale(
            product_id=product.id,
            seller_id=current_user.get("user_id"),
            quantity_sold=quantity_sold,
            status=StatusEnum.selling
        )
        db.add(new_sale)

        await db.commit()
        await db.refresh(new_sale)
        return new_sale
        
    
