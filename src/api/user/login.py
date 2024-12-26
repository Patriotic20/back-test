from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from src.base.db import get_db
from src.other.utils import authenticate_user, create_access_token
from datetime import datetime, timedelta
from src.base.config import settings


router = APIRouter()


@router.post("/login")
async def login(
    from_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    # Authenticate the user
    user = await authenticate_user(from_data.username, from_data.password, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password.",
        )

    access_token = create_access_token(
        {
            "sub": f"{user.last_name} {user.first_name}",
            "email": user.email,
            "exp": datetime.utcnow()
            + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
            "role": user.role.value,
            "user_id": str(user.id),
        }
    )

    return {"access_token": access_token, "token_type": "bearer"}
