import pandas as pd

from fastapi import APIRouter, UploadFile, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.base.db import get_db
from src.models.product import Product
from src.other.dependies import db_rollback

router = APIRouter()


@router.post("/upload-products")
@db_rollback
async def upload_products(file: UploadFile, db: AsyncSession = Depends(get_db)):
    data = _validate_file_data(file)

    errors = []
    for index, row in data.iterrows():
        row = _cast_row(row.to_dict())
        try:
            if any((pd.isna(val) for val in row.values())):
                raise ValueError("One or more required fields are missing.")

            product = Product(**row)
            db.add(product)

        except Exception as e:
            errors.append({"row": index + 1, "error": str(e)})

    if errors:
        return {"message": "File processed with some errors.", "errors": errors}

    return {"message": "File processed successfully!"}


def _validate_file_data(file: UploadFile):
    if not file.filename.endswith((".csv", ".xlsx")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file format. Use CSV or Excel.",
        )

    try:
        if file.filename.endswith(".csv"):
            data = pd.read_csv(file.file)
        else:
            data = pd.read_excel(file.file)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error reading file: {str(e)}",
        )

    required_columns = {"barcode", "name", "stock_quantity", "price", "category"}
    if not required_columns.issubset(data.columns):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File must include columns: {required_columns}",
        )

    return data


def _cast_row(data: dict):
    column_types = {
        "barcode": str,
        "name": str,
        "stock_quantity": int,
        "price": float,
        "category": str
    }

    for key, type_ in column_types.items():
        data[key] = type_(data[key])
    return data
