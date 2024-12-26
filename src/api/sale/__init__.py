from fastapi import APIRouter
from .create import router as create
from .read import router as read
from .update import router as update
from .delete import router as delete
from .confirm import router as confirm
from .payback import router as payback


router = APIRouter(prefix="/sale", tags=["Sale"])

router.include_router(create)
router.include_router(read)
router.include_router(update)
router.include_router(delete)
router.include_router(confirm)
router.include_router(payback)
