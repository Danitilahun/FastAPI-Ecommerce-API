import pytest
from fastapi.testclient import TestClient
from fastapi import status
import uuid

class TestUserOperations:
    """Test class for user operations."""

    @pytest.mark.parametrize(
        "user_data, expected_status",
        [
            ({"full_name": "John Doe", "username": f"john_doe_{uuid.uuid4()}", "email": f"john_{uuid.uuid4()}@example.com", "password": "password123"}, status.HTTP_201_CREATED),
            ({"full_name": "Jane Doe", "username": f"jane_doe_{uuid.uuid4()}", "email": f"jane_{uuid.uuid4()}@example.com", "password": "password123"}, status.HTTP_201_CREATED)
        ]
    )
    def test_create_user(self, client: TestClient, authenticated_admin_user: dict, user_data: dict, expected_status: int):
        """Test the creation of a user by an authenticated admin."""
        headers = {"Authorization": f"Bearer {authenticated_admin_user['access_token']}"}
        response = client.post("/users/", json=user_data, headers=headers)
        
        assert response.status_code == expected_status
        data = response.json()
        assert "message" in data
        assert data["message"] == f"{user_data['username']} with id {data['data']['id']} created successfully"
        assert data["data"]["username"] == user_data["username"]
    
    @pytest.mark.parametrize(
        "updated_data, expected_status",
        [
            ({"full_name": "John Updated", "email": f"john_updated_{uuid.uuid4()}@example.com"}, status.HTTP_200_OK),
            ({"full_name": "Jane Updated", "email": f"jane_updated_{uuid.uuid4()}@example.com"}, status.HTTP_200_OK)
        ]
    )
    def test_update_user(self, client: TestClient, authenticated_admin_user: dict, updated_data: dict, expected_status: int):
        """Test the update of a user by an authenticated admin."""
        
        # 1. Create a new user dynamically
        user_data = {
            "full_name": "Test User",
            "username": f"testuser_{uuid.uuid4()}",
            "email": f"testuser_{uuid.uuid4()}@example.com",
            "password": "password123"
        }
        headers = {"Authorization": f"Bearer {authenticated_admin_user['access_token']}"}
        
        # Create the user
        create_response = client.post("/users/", json=user_data, headers=headers)
        created_user = create_response.json()["data"]
        created_user_id = created_user["id"]  # Store the created user ID for update
        
        # 2. Use the created user's ID for the update operation
        response = client.put(f"/users/{created_user_id}", json=updated_data, headers=headers)

        # 3. Validate the update response
        assert response.status_code == expected_status
        data = response.json()
        assert data["data"]["full_name"] == updated_data["full_name"]
        assert data["data"]["email"] == updated_data["email"]

    def test_get_all_users(self, client: TestClient, authenticated_admin_user: dict):
        """Test that an admin can fetch all users."""
        headers = {"Authorization": f"Bearer {authenticated_admin_user['access_token']}"}
        response = client.get("/users/", headers=headers, params={"page": 1, "limit": 10})
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "message" in data
        assert "data" in data
        assert isinstance(data["data"], list)

    def test_delete_user(self, client: TestClient, authenticated_admin_user: dict):
        """Test the deletion of a user by an admin."""
        # First, create a user to delete
        user_data = {"full_name": "User To Delete", "username": "delete_user", "email": "delete@example.com", "password": "password123"}
        headers = {"Authorization": f"Bearer {authenticated_admin_user['access_token']}"}
        create_response = client.post("/users/", json=user_data, headers=headers)
        created_user = create_response.json()["data"]

        # Delete the created user
        response = client.delete(f"/users/{created_user['id']}", headers=headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["data"]["id"] == created_user["id"]
