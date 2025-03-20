import pytest
from fastapi.testclient import TestClient
from fastapi import status
import uuid

@pytest.mark.parametrize(
    "category_data, expected_status",
    [
        ({"name": f"Category {uuid.uuid4()}"}, status.HTTP_201_CREATED),
        ({"name": f"Category {uuid.uuid4()}"}, status.HTTP_201_CREATED)
    ]
)
def test_create_category(client: TestClient, authenticated_admin_user: dict, category_data: dict, expected_status: int):
    """Test the creation of a category by an authenticated admin."""
    headers = {"Authorization": f"Bearer {authenticated_admin_user['access_token']}"}
    response = client.post("/categories/", json=category_data, headers=headers)
    
    assert response.status_code == expected_status
    data = response.json()
    assert "message" in data
    assert data["message"] == f"{category_data['name']} with id {data['data']['id']} created successfully"
    assert data["data"]["name"] == category_data["name"]


@pytest.mark.parametrize(
    "updated_data, expected_status",
    [
        ({"name": f"Updated Category {uuid.uuid4()}"}, status.HTTP_200_OK),
        ({"name": f"Updated Category {uuid.uuid4()}"}, status.HTTP_200_OK)
    ]
)
def test_update_category(client: TestClient, authenticated_admin_user: dict, create_category: dict, updated_data: dict, expected_status: int):
    """Test the update of a category by an authenticated admin."""
    headers = {"Authorization": f"Bearer {authenticated_admin_user['access_token']}"}
    
    category_id = create_category["id"]
    response = client.put(f"/categories/{category_id}", json=updated_data, headers=headers)
    
    assert response.status_code == expected_status
    data = response.json()
    assert data["data"]["name"] == updated_data["name"]

def test_get_all_categories(client: TestClient, authenticated_user: dict):
    """Test that a normal user can fetch all categories."""
    headers = {"Authorization": f"Bearer {authenticated_user['access_token']}"}
    response = client.get("/categories/", headers=headers, params={"page": 1, "limit": 10})
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "message" in data
    assert "data" in data
    assert isinstance(data["data"], list)


def test_delete_category(client: TestClient, authenticated_admin_user: dict, create_category: dict):
    """Test the deletion of a category by an admin."""
    headers = {"Authorization": f"Bearer {authenticated_admin_user['access_token']}"}
    category_id = create_category["id"]

    response = client.delete(f"/categories/{category_id}", headers=headers)
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["data"]["id"] == category_id
