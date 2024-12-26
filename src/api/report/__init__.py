from fastapi import APIRouter
from .month import router as month
from .download_exel import router as download_exel

router = APIRouter(prefix="/report", tags=["Report"])

router.include_router(month)
router.include_router(download_exel)
