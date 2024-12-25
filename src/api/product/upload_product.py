from fastapi import APIRouter, UploadFile, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
import pandas as pd
from src.settings.db import get_db
from src.models.product import Product

router = APIRouter()

@router.post("/upload-products")
async def upload_products(
    file: UploadFile,
    db: AsyncSession = Depends(get_db)
):
    if not file.filename.endswith((".csv", ".xlsx")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file format. Use CSV or Excel."
        )

    try:
        if file.filename.endswith(".csv"):
            data = pd.read_csv(file.file)
        else:
            data = pd.read_excel(file.file)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error reading file: {str(e)}"
        )

    required_columns = {"barcode", "name", "stock_quantity", "price", "category"}
    if not required_columns.issubset(data.columns):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File must include columns: {required_columns}"
        )

    errors = []

    for index, row in data.iterrows():
        try:
            # Extract and validate row data
            barcode = row.get('barcode')
            name = row.get('name')
            stock_quantity = row.get('stock_quantity')
            price = row.get('price')
            category = row.get('category')

            if pd.isna(barcode) or pd.isna(name) or pd.isna(stock_quantity) or pd.isna(price) or pd.isna(category):
                raise ValueError("One or more required fields are missing.")

            # Create a new Product instance
            product = Product(
                name=name,
                barcode=str(barcode),
                stock_quantity=int(stock_quantity),
                price=float(price),
                category=category
            )

            db.add(product)

        except Exception as e:
            errors.append({"row": index + 1, "error": str(e)})

    try:
        await db.commit()
    except IntegrityError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error while updating"
        )

    if errors:
        return {
            "message": "File processed with some errors.",
            "errors": errors
        }

    return {"message": "File processed successfully!"}
