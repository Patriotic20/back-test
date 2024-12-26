import pytest
from sqlalchemy import select
from main import app
from src.models.user import User
from passlib.context import CryptContext

from fastapi.testclient import TestClient

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

client = TestClient(app)


@pytest.mark.asyncio
async def test_user_registration(db):
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "role": "seller",
        "email": "john.doe@example.com",
        "phone_number": "+998901234567",
        "hashed_password": "securepassword123",
    }

    response = client.post("/users/registration", json=user_data)

    assert response.status_code == 200

    response_data = response.json()
    assert response_data["first_name"] == user_data["first_name"]
    assert response_data["last_name"] == user_data["last_name"]
    assert response_data["role"] == user_data["role"]
    assert response_data["email"] == user_data["email"]
    assert response_data["phone_number"] == user_data["phone_number"]

    user_in_db = await db.execute(select(User).where(User.email == user_data["email"]))

    user_in_db = user_in_db.scalars().first()

    assert user_in_db is not None
    assert user_in_db.first_name == user_data["first_name"]
    assert user_in_db.last_name == user_data["last_name"]
    assert pwd_context.verify(user_data["hashed_password"], user_in_db.hashed_password)



async def test_registration_conflict(db):
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "role": "seller",
        "email": "john.doe@example.com",
        "phone_number": "+998901234567",
        "hashed_password": "securepassword123",
    }
    
    response = client.post("/users/registration", json=user_data)
    
    assert response.status_code == 409
    assert response.json() == {"detail": "This user already exists"}
    
    user_in_db = await db.execute(select(User).where(User.email == user_data["email"]))

    user_in_db = user_in_db.scalars().first()

    assert user_in_db is not None
    assert user_in_db.first_name == user_data["first_name"]
    assert user_in_db.last_name == user_data["last_name"]
    assert pwd_context.verify(user_data["hashed_password"], user_in_db.hashed_password)