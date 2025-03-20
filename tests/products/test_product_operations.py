import pytest
from fastapi.testclient import TestClient
import uuid
from fastapi import status
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
import uuid
from datetime import datetime
from fastapi import status

@pytest.mark.parametrize(
    "product_data, expected_status",
    [
        (
            {
                "title": f"Test Product {uuid.uuid4()}",
                "description": "Test description 1",
                "price": 100,
                "discount_percentage": 20.0,
                "rating": 4.5,
                "stock": 50,
                "brand": "Test Brand 1",
                "thumbnail": "test_thumbnail_1.png",
                "images": ["test_image_1.png"],
                "is_published": True,
                "category_id": 1,
                "created_at": datetime.utcnow().isoformat()  # Adding created_at
            },
            status.HTTP_201_CREATED
        ),
        (
            {
                "title": f"Test Product {uuid.uuid4()}",
                "description": "Test description 2",
                "price": 200,
                "discount_percentage": 15.0,
                "rating": 4.0,
                "stock": 30,
                "brand": "Test Brand 2",
                "thumbnail": "test_thumbnail_2.png",
                "images": ["test_image_2.png"],
                "is_published": False,
                "category_id": 2,
                "created_at": datetime.utcnow().isoformat()  # Adding created_at
            },
            status.HTTP_201_CREATED
        ),
        (
            {
                "title": f"Test Product {uuid.uuid4()}",
                "description": "Test description 3",
                "price": 300,
                "discount_percentage": 10.0,
                "rating": 5.0,
                "stock": 60,
                "brand": "Test Brand 3",
                "thumbnail": "test_thumbnail_3.png",
                "images": ["test_image_3.png"],
                "is_published": True,
                "category_id": 3,
                "created_at": datetime.utcnow().isoformat()  # Adding created_at
            },
            status.HTTP_201_CREATED
        ),
    ]
)
def test_create_product(client: TestClient, authenticated_admin_user: dict, create_category: dict, product_data: dict, expected_status: int):
    """Test that an admin user can create a product."""
    headers = {"Authorization": f"Bearer {authenticated_admin_user['access_token']}"}
    
    # Ensure category_id in product_data corresponds to the ID of an existing category
    product_data["category_id"] = create_category["id"]

    response = client.post("/products/", json=product_data, headers=headers)

    # Print response details for debugging
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Body: {response.json()}")

    assert response.status_code == expected_status
    data = response.json()
    assert data["data"]["title"] == product_data["title"]
    assert data["data"]["category_id"] == product_data["category_id"]


@pytest.mark.parametrize(
    "updated_data, expected_status",
    [
        (
            {
                "title": "Updated Product",
                "description": "Updated description",
                "price": 150,
                "discount_percentage": 10.0,
                "rating": 4.7,
                "stock": 60,
                "brand": "Updated Brand",
                "thumbnail": "updated_thumbnail.png",
                "images": ["updated_image.png"],
                "is_published": True,
                "category_id": 87  # Will be replaced by fixture
            },
            status.HTTP_200_OK
        ),
    ]
)
def test_update_product(
        client: TestClient,
        authenticated_admin_user: dict,
        create_category: dict,
        create_product: dict,
        updated_data: dict,
        expected_status: int
):
    headers = {"Authorization": f"Bearer {authenticated_admin_user['access_token']}"}
    
    # Use dynamic category ID
    updated_data["category_id"] = create_category["id"]
    
    # Get valid product ID from fixture
    product_id = create_product["id"]
    
    response = client.put(
        f"/products/{product_id}",
        json=updated_data,
        headers=headers
    )
    
    print("hello",response.json())
    
    assert response.status_code == expected_status
    response_data = response.json()["data"]
    
    # Verify updated fields
    for key in updated_data:
        if key == "images":
            assert set(response_data[key]) == set(updated_data[key])
        else:
            assert response_data[key] == updated_data[key]
            
# Test for getting all products
def test_get_all_products(client: TestClient, authenticated_user: dict):
    """Test that a normal user can fetch all products."""
    headers = {"Authorization": f"Bearer {authenticated_user['access_token']}"}
    response = client.get("/products/", headers=headers, params={"page": 1, "limit": 10})
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "message" in data
    assert "data" in data
    assert isinstance(data["data"], list)

# Test for getting a specific product by ID (Normal user)
def test_get_product(client: TestClient, authenticated_admin_user: dict, create_category: dict):
    """Test that a normal user can retrieve a product by its ID."""
    
    headers = {"Authorization": f"Bearer {authenticated_admin_user['access_token']}"}

    # Prepare product data for creation
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
        "created_at": datetime.utcnow().isoformat()  # Adding created_at to make it valid
    }

    # Create the product
    response = client.post("/products/", json=product_data, headers=headers)
    created_product = response.json()["data"]
    product_id = created_product["id"]  # Store the created product's ID for fetching

    # Fetch the created product by ID
    response = client.get(f"/products/{product_id}", headers=headers)
    
    # Print response details for debugging
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Body: {response.json()}")
    
    # Assertions
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    print("data new " , data)
    
    # Ensure the fetched product matches the created product
    assert data["data"]["id"] == product_id
    assert data["data"]["title"] == product_data["title"]
    assert data["data"]["category_id"] == product_data["category_id"]

# Test for deleting a product (Admin only)
def test_delete_product(client: TestClient, authenticated_admin_user: dict, create_category: dict, create_product: dict):
    """Test the deletion of a product by an admin."""
    
    headers = {"Authorization": f"Bearer {authenticated_admin_user['access_token']}"}

    # The created product ID will be used for the deletion
    product_id = create_product["id"]
    
    # Perform delete request
    response = client.delete(f"/products/{product_id}", headers=headers)
    
    # Print response details for debugging
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Body: {response.json()}")
    
    # Assert the response status is OK
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    # Ensure the correct product has been deleted by ID
    assert data["data"]["id"] == product_id
    assert "message" in data

