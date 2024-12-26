from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.base.db import get_db
from sqlalchemy import select
from src.models.user import User
from datetime import datetime, timedelta
from src.base.config import settings
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
import secrets
import string
import random

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)


async def authenticate_user(
    username: str, password: str, db: AsyncSession = Depends(get_db)
):
    user_query = await db.execute(select(User).where(User.email == username))
    user = user_query.scalars().first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    return user


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    jwt_encode = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return jwt_encode


def decode_token(token: str):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def generate_password(length=12):
    if length < 4:
        raise ValueError("Password length should be at least 4 characters.")

    # Define character pools
    letters = string.ascii_letters  # a-z, A-Z
    digits = string.digits  # 0-9
    special_chars = string.punctuation  # Special characters like !, @, #
    all_chars = letters + digits + special_chars

    # Ensure the password has at least one letter, digit, and special character
    password = [
        secrets.choice(letters),
        secrets.choice(digits),
        secrets.choice(special_chars),
    ]

    # Fill the rest of the password length with random choices
    password += [secrets.choice(all_chars) for _ in range(length - 3)]

    # Shuffle the password to avoid predictable patterns
    secrets.SystemRandom().shuffle(password)

    return "".join(password)


def random_number():
    my_list = []

    for _ in range(13):
        num = random.randint(0, 9)
        my_list.append(str(num))

    return "".join(my_list)
