from fastapi import APIRouter, Depends, HTTPException, status
from src.schemas.user import UserResponse, UserCreate
from src.models.user import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.base.db import get_db


router = APIRouter()


@router.post("/registration", response_model=UserResponse)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    user_info = await db.execute(
        select(User).where(
            User.first_name == user.first_name,
            User.last_name == user.last_name,
            User.phone_number == user.phone_number,
        )
    )
    user_info = user_info.scalars().first()
    if user_info:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="This user already exists"
        )
    new_user = User(**user.model_dump())
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user
