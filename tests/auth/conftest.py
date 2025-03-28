import pytest
import uuid
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def new_user():
    """Fixture to provide common user data with unique identifiers."""
    unique_id = str(uuid.uuid4())  # Generate a unique ID
    return {
        "full_name": f"Test User {unique_id}",
        "username": f"testuser_{unique_id}",
        "email": f"testuser_{unique_id}@example.com",
        "password": "testpassword123"
    }

@pytest.fixture
def create_test_user(client: TestClient, new_user: dict):
    """Fixture to create a test user before login tests."""
    client.post("/auth/signup", json=new_user)  # Ensure the user exists before login
    return new_user

@pytest.fixture
def authenticated_user(client: TestClient, create_test_user: dict):
    """Fixture to authenticate a user and get the access token."""
    form_data = {
        "username": create_test_user["username"],
        "password": create_test_user["password"]
    }
    response = client.post("/auth/login", data=form_data)  # Login to get tokens
    assert response.status_code == 200
    return response.json()  # Returning the full response with tokens
