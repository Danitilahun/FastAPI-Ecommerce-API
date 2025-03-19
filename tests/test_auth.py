import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.schemas.auth import Signup
from app.models.models import User
from app.core.security import get_password_hash
from sqlalchemy.orm import Session
from fastapi import status
from app.db.database import get_db

import uuid

# Fixture to generate a unique user for each test
@pytest.fixture
def new_user():
    unique_id = str(uuid.uuid4()) 
    return {
        "full_name": "Test User",
        "username": f"testuser_{unique_id}",
        "email": f"testuser_{unique_id}@example.com",  # Ensure unique email
        "password": "testpassword123"
    }

# Test 1: Successful Signup
def test_signup(client: TestClient, new_user: dict):
    response = client.post("/auth/signup", json=new_user)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "message" in data
    assert new_user["username"] in data["message"]
    assert f"with id" in data["message"]
    assert "created successfully" in data["message"]
    assert "data" in data
    assert data["data"]["username"] == new_user["username"]

# Test 2: Signup with Existing Username/Email
def test_signup_existing_user(client: TestClient, new_user: dict):
    # First, create the user
    client.post("/auth/signup", json=new_user)

    # Try signing up again with the same username/email
    response = client.post("/auth/signup", json=new_user)
    print(response)
    assert response.status_code == status.HTTP_409_CONFLICT
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Username or email already exists."
