from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.base.db import get_db
from sqlalchemy import select
from src.models.sale import PaymentMethod, Sale, StatusEnum
from src.other.dependies import require_role, get_current_user
from src.other.errorrs import handle_exceptions
from sqlalchemy.exc import SQLAlchemyError


router = APIRouter()


@router.patch("/", dependencies=[Depends(require_role("Seller"))])
@handle_exceptions
async def update_sale(
    quantity: int | None = None,
    payment_method: PaymentMethod | None = None,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        sale = await db.execute(
            select(Sale).where(Sale.seller_id == current_user.get("user_id"))
        )
        sale = sale.scalars().first()

        if sale is None:
            raise ValueError("Sale not found")

        if sale.status == StatusEnum.selling and sale.seller_id == current_user.get(
            "user_id"
        ):
            if quantity:
                sale.quantity_sold = quantity
            if payment_method:
                sale.payment_method = payment_method

            await db.commit()
            await db.refresh(sale)
            return sale
        else:
            raise ValueError("Sale cannot be updated")

    except SQLAlchemyError as e:
        await db.rollback()
        return {"error": f"Database error: {str(e)}"}
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}
