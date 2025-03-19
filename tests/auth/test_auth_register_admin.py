from fastapi.testclient import TestClient
from fastapi import status


class TestAuthRegisterAdmin:
    """Test class for registering admin functionality"""

    # Test 1: Successful Admin Registration
    def test_register_admin(self, client: TestClient, new_user: dict):
        """Test successful admin registration"""
        # Add 'admin' flag to the user data to specify it's for admin registration
        admin_data = new_user.copy()
        admin_data["role"] = "admin"
        
        response = client.post("/auth/register-admin", json=admin_data)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert "message" in data
        assert "created successfully" in data["message"]
        assert "data" in data
        assert data["data"]["username"] == admin_data["username"]
        assert data["data"]["role"] == "admin"

    # Test 2: Register Admin with Existing Username/Email
    def test_register_admin_existing_user(self, client: TestClient, new_user: dict):
        """Test duplicate admin registration attempt"""
        # First, create the user as a regular user
        client.post("/auth/signup", json=new_user)

        # Now, try registering the same user as an admin
        admin_data = new_user.copy()
        admin_data["role"] = "admin"
        
        response = client.post("/auth/register-admin", json=admin_data)
        assert response.status_code == status.HTTP_409_CONFLICT
        data = response.json()
        assert "detail" in data
        assert data["detail"] == "Username or email already exists."
