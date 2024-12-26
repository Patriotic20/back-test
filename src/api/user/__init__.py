from fastapi import APIRouter
from .create import router as create
from .read import router as read
from .update import router as update
from .delete import router as delete
from .login import router as login


router = APIRouter(prefix="/users", tags=["Users"])

router.include_router(create)
router.include_router(read)
router.include_router(update)
router.include_router(delete)
router.include_router(login)
