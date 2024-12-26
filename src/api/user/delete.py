from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.base.db import get_db
from src.models.user import User
from sqlalchemy import select
import uuid

router = APIRouter()


@router.delete("/{user_id}")
async def delete_user(user_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    user = await db.execute(select(User).where(User.id == user_id))
    user = user.scalars().first()
    await db.delete(user)
    await db.commit()
