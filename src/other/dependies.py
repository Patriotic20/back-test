from fastapi import Depends , HTTPException , status
from src.other.utils import oauth2_scheme , decode_token
from sqlalchemy import select
from src.models import User
from sqlalchemy.ext.asyncio import AsyncSession 
from src.settings.db import get_db



async def get_current_user(token :str = Depends(oauth2_scheme) , db : AsyncSession= Depends(get_db)):
    payload = decode_token(token)
    username : str = payload.get("sub")
    email : str = payload.get("email")
    role : str = payload.get("role")
    user_id : str = payload.get("user_id")

    user = await db.execute(select(User).where(User.id == user_id))
    user = user.scalars().first()
    
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="UserInvalid authentication"
        )
    return {"username": username, "role":role, "user_id":user_id , "email" : email}

def require_role(required_role: str):
    def role_checker(user=Depends(get_current_user)):
        if user["role"] != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access forbidden: Requires {required_role} role",
            )
        return user
    return role_checker