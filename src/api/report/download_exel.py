from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import Sale, User, Product
from src.base.db import get_db
from sqlalchemy import select
from io import BytesIO
import pandas as pd


router = APIRouter()


@router.get("/download-sales/")
async def download_sales(
    db: AsyncSession = Depends(get_db),
    with_sale_id: bool = Query(True, description="Include sale ID in the result"),
):
    # Join Sale with Product and User models to get names
    query = (
        select(
            Sale, Product.name.label("product_name"), User.username.label("user_name")
        )
        .join(Product, Product.id == Sale.product_id)
        .join(User, User.id == Sale.seller_id)
    )

    result = await db.execute(query)
    sales = result.fetchall()

    # Convert the result to a pandas DataFrame
    sale_data = []
    for sale, product_name, user_name in sales:
        sale_entry = {
            "product_name": product_name,
            "user_name": user_name,
            "quantity_sold": sale.quantity_sold,
            "sale_date": sale.sale_date,
            "payment_method": sale.payment_method,
            "discount": sale.discount,
            "tax": sale.tax,
            "status": sale.status.value,
            "random_numbers": sale.random_numbers,
        }
        if with_sale_id:
            sale_entry["sale_id"] = str(sale.id)

        sale_data.append(sale_entry)

    df = pd.DataFrame(sale_data)

    # Save DataFrame to a BytesIO object in Excel format
    output = BytesIO()
    df.to_excel(output, index=False, engine="openpyxl")
    output.seek(0)

    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=sales.xlsx"},
    )
