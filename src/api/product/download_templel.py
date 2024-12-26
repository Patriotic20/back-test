from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import pandas as pd
import io

router = APIRouter()


@router.get("/download-template-excel")
def download_template_excel():
    df = pd.DataFrame(
        columns=["barcode", "name", "stock_quantity", "price", "category"]
    )

    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Template")
    buffer.seek(0)

    headers = {"Content-Disposition": "attachment; filename=inventory_template.xlsx"}
    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers=headers,
    )
