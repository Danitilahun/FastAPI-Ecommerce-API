from fastapi.testclient import TestClient
from fastapi import status

class TestAuthRefreshToken:
    """Test class for refresh token functionality"""

    def test_refresh_token_valid(self, client: TestClient, authenticated_user: dict):
        """Test valid token refresh"""
        # Verify login response contains refresh token
        assert "refresh_token" in authenticated_user
        
        headers = {"refresh-token": authenticated_user["refresh_token"]}
        response = client.post("/auth/refresh", headers=headers)
        
        print("response" , response)
        
        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response.json()

    def test_refresh_token_invalid(self, client: TestClient):
        """Test invalid refresh token"""
        headers = {"refresh-token": "invalid_token"}
        response = client.post("/auth/refresh", headers=headers)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "WWW-Authenticate" in response.headers
        assert response.json()["detail"] == "Invalid refresh token."