from src.models.user import UserRole
from pydantic import BaseModel, field_validator, Field, EmailStr
from passlib.context import CryptContext

import uuid
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserBase(BaseModel):
    last_name: str
    first_name: str
    role: UserRole
    email: EmailStr
    phone_number: str = Field(..., pattern=r"^\+998\d{2}\s?\d{3}\s?\d{2}\s?\d{2}$")


class UserCreate(UserBase):
    hashed_password: str

    @field_validator("hashed_password")
    def hash_password(cls, value: str) -> str:
        return pwd_context.hash(value)


class UserResponse(UserBase):
    id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True
