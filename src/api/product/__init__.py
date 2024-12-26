from fastapi import APIRouter
from .create import router as create
from .read import router as read
from .upload_product import router as upload_product
from .update import router as update
from .download_templel import router as download_templel

router = APIRouter(tags=["Product"])


router.include_router(create)
router.include_router(read)
router.include_router(update)
router.include_router(upload_product)
router.include_router(download_templel)
