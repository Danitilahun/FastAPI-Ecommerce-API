from fastapi.testclient import TestClient
from fastapi import status

class TestAuthLogin:
    """Test class for authentication login functionality"""

    def test_login_successful(self, client: TestClient, create_test_user: dict):
        """Test successful login with correct credentials"""
        form_data = {
            "username": create_test_user["username"],
            "password": create_test_user["password"]
        }
        response = client.post("/auth/login", data=form_data) # Use data instead of json
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert "token_type" in data
        assert data["token_type"] == "Bearer"

    def test_login_invalid_username(self, client: TestClient, create_test_user: dict):
        """Test login with incorrect username"""
        form_data = {
            "username": "wrong_username",
            "password": create_test_user["password"]
        }
        response = client.post("/auth/login", data=form_data)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        data = response.json()
        assert "detail" in data
        assert data["detail"] == "Invalid Credentials"

    def test_login_invalid_password(self, client: TestClient, create_test_user: dict):
        """Test login with incorrect password"""
        form_data = {
            "username": create_test_user["username"],
            "password": "wrong_password"
        }
        response = client.post("/auth/login", data=form_data)
        assert response.status_code == status.HTTP_403_FORBIDDEN
        data = response.json()
        assert "detail" in data
        assert data["detail"] == "Invalid Credentials"