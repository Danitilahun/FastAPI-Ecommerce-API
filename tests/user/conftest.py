import pytest
from fastapi.testclient import TestClient
import uuid

@pytest.fixture
def new_user():
    """Fixture to provide common user data with unique identifiers."""
    unique_id = str(uuid.uuid4()) 
    return {
        "full_name": f"Test User {unique_id}",
        "username": f"testuser_{unique_id}",
        "email": f"testuser_{unique_id}@example.com",
        "password": "testpassword123"
    }

@pytest.fixture
def create_test_user(client: TestClient, new_user: dict):
    """Fixture to create a test user before login tests."""
    client.post("/auth/signup", json=new_user) 
    return new_user

@pytest.fixture
def create_admin_user(client: TestClient, new_user: dict):
    """Fixture to create an admin user for testing user-related routes."""
    admin_data = new_user.copy()
    admin_data["role"] = "admin"
    client.post("/auth/register-admin", json=admin_data)
    return admin_data

@pytest.fixture
def authenticated_admin_user(client: TestClient, create_admin_user: dict):
    """Fixture to log in an admin user and retrieve tokens."""
    form_data = {
        "username": create_admin_user["username"],
        "password": create_admin_user["password"]
    }
    response = client.post("/auth/login", data=form_data)
    assert response.status_code == 200
    return response.json()
