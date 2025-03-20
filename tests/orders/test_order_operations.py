from datetime import datetime
import uuid
from fastapi import status
from fastapi.testclient import TestClient
from app.schemas.orders import OrderOut, OrdersOutList

def test_create_order(client: TestClient, authenticated_admin_user: dict, create_category: dict, create_product: dict):
    """Test that a normal user can create an order after an admin creates the product."""
    headers = {"Authorization": f"Bearer {authenticated_admin_user['access_token']}"}

    # Ensure product data has already been created via the create_product fixture
    product_id = create_product["id"]
    print("product_id", product_id)

    # Create the order with the product added
    order_data = {
        "order_items": [
            {"product_id": product_id, "quantity": 1}
        ]
    }

    # Make the POST request to create an order
    response = client.post("/orders/", json=order_data, headers=headers)

    # Print response details for debugging
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Body: {response.json()}")

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert "data" in data
    assert data["data"]["total_amount"] > 0 
    assert len(data["data"]["order_items"]) == 1 
    
def test_get_all_orders(client: TestClient, authenticated_admin_user: dict):
    """Test that a normal user can fetch all their orders."""
    headers = {"Authorization": f"Bearer {authenticated_admin_user['access_token']}"}
    response = client.get("/orders/", headers=headers, params={"page": 1, "limit": 10})
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "message" in data
    assert "data" in data
    assert isinstance(data["data"], list)
    
def test_get_order_by_id(client: TestClient, authenticated_admin_user: dict, create_product: dict, create_category: dict):
    """Test that a normal user can retrieve a specific order by ID."""
    headers = {"Authorization": f"Bearer {authenticated_admin_user['access_token']}"}
    
    # Create a product for the order
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

    # Create the product
    response = client.post("/products/", json=product_data, headers=headers)
    created_product = response.json()["data"]
    product_id = created_product["id"]

    # Create an order with the created product
    order_data = {
        "order_items": [{"product_id": product_id, "quantity": 1}]
    }

    response = client.post("/orders/", json=order_data, headers=headers)
    created_order = response.json()["data"]
    order_id = created_order["id"]

    # Fetch the specific order by ID
    response = client.get(f"/orders/{order_id}", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["data"]["id"] == order_id


def test_update_order(client: TestClient, authenticated_admin_user: dict, create_product: dict, create_category: dict):
    """Test that a normal user can update an order."""
    headers = {"Authorization": f"Bearer {authenticated_admin_user['access_token']}"}
    
    # Create a product for the order
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

    # Create the product
    response = client.post("/products/", json=product_data, headers=headers)
    created_product = response.json()["data"]
    product_id = created_product["id"]

    # Create an order with the created product
    order_data = {
        "order_items": [{"product_id": product_id, "quantity": 1}]
    }

    response = client.post("/orders/", json=order_data, headers=headers)
    created_order = response.json()["data"]
    order_id = created_order["id"]

    # Update the order
    updated_order_data = {
        "order_items": [{"product_id": product_id, "quantity": 2}]  # Update quantity
    }

    response = client.put(f"/orders/{order_id}", json=updated_order_data, headers=headers)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["data"]["order_items"][0]["quantity"] == 2  # Check if the quantity was updated
    
    
def test_delete_order(client: TestClient, authenticated_admin_user: dict, create_product: dict, create_category: dict):
    """Test that a normal user can delete an order."""
    headers = {"Authorization": f"Bearer {authenticated_admin_user['access_token']}"}
    
    # Create a product for the order
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

    # Create the product
    response = client.post("/products/", json=product_data, headers=headers)
    created_product = response.json()["data"]
    product_id = created_product["id"]

    # Create an order with the created product
    order_data = {
        "order_items": [{"product_id": product_id, "quantity": 1}]
    }

    response = client.post("/orders/", json=order_data, headers=headers)
    created_order = response.json()["data"]
    order_id = created_order["id"]

    # Delete the created order
    response = client.delete(f"/orders/{order_id}", headers=headers)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["data"]["id"] == order_id

