from datetime import datetime
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
def authenticated_user(client: TestClient, create_test_user: dict):
    """Fixture to log in a normal user and retrieve tokens."""
    form_data = {
        "username": create_test_user["username"],
        "password": create_test_user["password"]
    }
    response = client.post("/auth/login", data=form_data)
    assert response.status_code == 200
    return response.json()


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

@pytest.fixture
def create_category(client: TestClient, authenticated_admin_user: dict):
    """Fixture to create a category."""
    category_data = {"name": f"Category {uuid.uuid4()}"}
    headers = {"Authorization": f"Bearer {authenticated_admin_user['access_token']}"}
    response = client.post("/categories/", json=category_data, headers=headers)
    assert response.status_code == 201
    return response.json()["data"]

@pytest.fixture
def create_product(client: TestClient, authenticated_admin_user: dict, create_category: dict):
    """Fixture to create a product."""
    product_data = {
        "title": f"Test Product {uuid.uuid4()}",
        "description": "Test description",
        "price": 100,
        "discount_percentage": 20.0,
        "rating": 4.5,
        "stock": 50,
        "brand": "Test Brand",
        "thumbnail": "test_thumbnail.png",
        "images": ["test_image.png"],
        "is_published": True,
        "category_id": create_category["id"],
        "created_at": datetime.utcnow().isoformat()
    }

    headers = {"Authorization": f"Bearer {authenticated_admin_user['access_token']}"}
    response = client.post("/products/", json=product_data, headers=headers)
    
    assert response.status_code == 201
    return response.json()["data"]