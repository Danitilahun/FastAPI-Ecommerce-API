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
from pydantic import ValidationError


@pytest.fixture
def new_user():
    unique_id = str(uuid.uuid4())
    return {
        "full_name": "Test User",
        "username": f"testuser_{unique_id}",
        "email": f"testuser_{unique_id}@example.com",
        "password": "testpassword123"
    }

class TestAuthSignup:
    """Test class for authentication signup functionality"""

    # Test 1: Successful Signup
    def test_signup(self, client: TestClient, new_user: dict):
        """Test successful user registration"""
        response = client.post("/auth/signup", json=new_user)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "message" in data
        assert new_user["username"] in data["message"]
        assert "with id" in data["message"]
        assert "created successfully" in data["message"]
        assert "data" in data
        assert data["data"]["username"] == new_user["username"]

    # Test 2: Signup with Existing Username/Email
    def test_signup_existing_user(self, client: TestClient, new_user: dict):
        """Test duplicate user registration attempt"""
        # First, create the user
        client.post("/auth/signup", json=new_user)

        # Try signing up again with the same credentials
        response = client.post("/auth/signup", json=new_user)
        assert response.status_code == status.HTTP_409_CONFLICT
        data = response.json()
        assert "detail" in data
        assert data["detail"] == "Username or email already exists."

    # Test 3: Signup with Invalid Email Format
    def test_signup_invalid_email(self, client: TestClient, new_user: dict):
        """Test registration with an invalid email address"""
        new_user["email"] = "invalid-email"
        response = client.post("/auth/signup", json=new_user)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # Test 4: Signup with Short Password
    def test_signup_short_password(self, client: TestClient, new_user: dict):
        """Test registration with a password that is too short"""
        new_user["password"] = "short"
        response = client.post("/auth/signup", json=new_user)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    # Test 5: Signup with Missing Fields
    def test_signup_missing_fields(self, client: TestClient):
        """Test registration with missing required fields"""
        incomplete_user = {
            "username": "testuser",
            "email": "test@example.com",
        }  # Missing full_name and password
        response = client.post("/auth/signup", json=incomplete_user)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY