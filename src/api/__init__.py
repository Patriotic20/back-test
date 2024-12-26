from fastapi import APIRouter
from .user import router as user_api
from .product import router as product_api
from .sale import router as sale_api
from .report import router as report_api


router = APIRouter()

router.include_router(user_api)
router.include_router(product_api)
router.include_router(sale_api)
router.include_router(report_api)
