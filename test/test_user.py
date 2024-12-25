import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from main import app
from src.schemas.user import UserCreate
from unittest.mock import MagicMock
from src.models.user import User


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client
        
@pytest.fixture
def mock_get_db():
    mock_db = MagicMock()
    yield mock_db

import httpx

@pytest.mark.asyncio
async def test_registration_conflict_1():
    async with httpx.AsyncClient() as client:
        response = await client.post("/register", json={"email": "test@example.com", "password": "password123"})
        assert response.status_code == 409

    
def test_registration_success(client , mock_get_db):        
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "phone_number": "+998947413736",
        "email": "johndoe@example.com",
        "role": "manager",
        "hashed_password": "securepassword"
    }
    
    mock_get_db.execute.return_value.scalars.return_value.first.return_value = None

    response = client.post("users/registration", json=user_data)
    print(response.json())
    
    
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["first_name"] == user_data["first_name"]
    assert response_data["last_name"] == user_data["last_name"]
    assert response_data["phone_number"] == user_data["phone_number"]
    assert response_data["email"] == user_data["email"]
    assert response_data["role"] == user_data["role"]
    assert "id" in response_data  # Ensure an ID is returned for the new user
    assert "created_at" in response_data 
    
    # assert response_data["hashed_password"] != "securepassword"
    
    

def test_registration_conflict(client):    
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "phone_number": "+998947413736",
        "email": "johndoe@example.com",
        "role": "manager",
        "hashed_password": "securepassword"
    }
    
    existing_user = MagicMock()
    existing_user.first_name = "John"
    existing_user.last_name = "Doe"
    existing_user.phone_number = "+998947413736"
    existing_user.email = "johndoe@example.com"
    
    # mock_get_db.execute.return_value.scalars.return_value.first.return_value = existing_user
    
    response = client.post("users/registration", json=user_data)
    
    assert response.status_code == 409 
    assert response.json() == {"detail" : "This user already exists"}
    
def test_registration_invalid_role(client):
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "phone_number": "+99890 123 45 67",
        "email": "johndoe@example.com",
        "role": "admin",  # Invalid role
        "hashed_password": "securepassword"
    }
    
    response = client.post("users/registration", json=user_data)
    
    assert response.status_code == 422
    assert "detail" in response.json()
    