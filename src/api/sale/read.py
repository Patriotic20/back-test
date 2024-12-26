from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.base.db import get_db
from src.models import Sale, Product
from src.other.errorrs import handle_exceptions
from src.other.dependies import require_role

router = APIRouter()


@handle_exceptions
@router.get("/read", dependencies=[Depends(require_role("Seller"))])
async def read_sale(db: AsyncSession = Depends(get_db)):
    try:
        query = select(Sale).join(Product)
        result = await db.execute(query)
        sales = result.scalars().all()

        if not sales:
            raise HTTPException(
                status_code=404, detail="No sales found for the given barcode"
            )

        return sales

    except Exception as e:
        # If an error occurs, raise a 500 internal server error
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
