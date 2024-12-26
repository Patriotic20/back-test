from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.base.db import get_db
from src.models import Sale
from src.models.sale import StatusEnum, PaymentMethod
from src.other.errorrs import handle_exceptions
from src.other.dependies import require_role, get_current_user
from src.other.utils import random_number

router = APIRouter()


@handle_exceptions
@router.patch("/confirm", dependencies=[Depends(require_role("seller"))])
async def confirm_sold(
    confirm: bool = Query(..., description="Confirmation flag to mark sales as sold"),
    payment_method: PaymentMethod = Query(
        ..., description="Payment method for the sale"
    ),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    if not confirm:
        raise HTTPException(status_code=400, detail="Confirmation flag must be True.")

    # Fetch sales for the current seller that are in 'selling' status
    sales_query = select(Sale).where(
        Sale.seller_id == current_user.get("user_id"), Sale.status == StatusEnum.selling
    )
    sales_result = await db.execute(sales_query)
    sales = sales_result.scalars().all()

    if not sales:
        raise HTTPException(
            status_code=404,
            detail=f"No sales found for seller ID {current_user.get('user_id')}.",
        )

    # Generate a random number (e.g., invoice number)
    random_number_value = random_number()

    # Update sales
    for sale in sales:
        sale.status = StatusEnum.sold
        sale.payment_method = payment_method
        sale.random_numbers = random_number_value
        db.add(sale)  # Add the updated sale to the session

    await db.flush()

    await db.commit()  # Commit the changes to the database

    for sale in sales:
        await db.refresh(sale)
    return {"message": "Sales confirmed as sold", "sales": sales}
