import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.db import db_service
import tempfile
import os

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    """Setup test database before each test"""
    # Create a temporary database for testing
    temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
    db_service.db_path = temp_db.name
    db_service.init_database()
    
    yield
    
    # Cleanup after test
    temp_db.close()
    os.unlink(temp_db.name)

def test_create_product():
    """Test creating a new product"""
    product_data = {
        "name": "Test Product",
        "description": "A test product for testing",
        "category": "Test Category",
        "price": 9.99,
        "stock_quantity": 10,
        "shelf_location": "A1",
        "barcode": "123456789"
    }
    
    response = client.post("/products/", json=product_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Product created successfully"
    assert data["data"]["name"] == product_data["name"]
    assert data["data"]["id"] is not None

def test_get_products():
    """Test getting all products"""
    # Create a test product first
    product_data = {
        "name": "Test Product",
        "description": "A test product",
        "category": "Test",
        "price": 5.99,
        "stock_quantity": 5
    }
    client.post("/products/", json=product_data)
    
    response = client.get("/products/")
    assert response.status_code == 200
    
    data = response.json()
    assert data["success"] is True
    assert len(data["data"]) >= 1
    assert data["total"] >= 1

def test_get_product_by_id():
    """Test getting a specific product by ID"""
    # Create a test product first
    product_data = {
        "name": "Specific Product",
        "description": "A specific test product",
        "category": "Specific",
        "price": 15.99,
        "stock_quantity": 20
    }
    create_response = client.post("/products/", json=product_data)
    product_id = create_response.json()["data"]["id"]
    
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["success"] is True
    assert data["data"]["id"] == product_id
    assert data["data"]["name"] == product_data["name"]

def test_get_nonexistent_product():
    """Test getting a product that doesn't exist"""
    response = client.get("/products/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"

def test_update_product():
    """Test updating a product"""
    # Create a test product first
    product_data = {
        "name": "Update Test Product",
        "description": "A product to update",
        "category": "Update Test",
        "price": 25.99,
        "stock_quantity": 15
    }
    create_response = client.post("/products/", json=product_data)
    product_id = create_response.json()["data"]["id"]
    
    # Update the product
    update_data = {
        "price": 29.99,
        "stock_quantity": 20,
        "description": "Updated description"
    }
    
    response = client.put(f"/products/{product_id}", json=update_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["success"] is True
    assert data["data"]["price"] == 29.99
    assert data["data"]["stock_quantity"] == 20
    assert data["data"]["description"] == "Updated description"

def test_update_nonexistent_product():
    """Test updating a product that doesn't exist"""
    update_data = {"price": 99.99}
    response = client.put("/products/999", json=update_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"

def test_delete_product():
    """Test deleting a product"""
    # Create a test product first
    product_data = {
        "name": "Delete Test Product",
        "description": "A product to delete",
        "category": "Delete Test",
        "price": 35.99,
        "stock_quantity": 8
    }
    create_response = client.post("/products/", json=product_data)
    product_id = create_response.json()["data"]["id"]
    
    # Delete the product
    response = client.delete(f"/products/{product_id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Product deleted successfully"
    
    # Verify the product is deleted
    get_response = client.get(f"/products/{product_id}")
    assert get_response.status_code == 404

def test_delete_nonexistent_product():
    """Test deleting a product that doesn't exist"""
    response = client.delete("/products/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"

def test_search_products():
    """Test searching products"""
    # Create test products
    products = [
        {"name": "Apple Juice", "description": "Fresh apple juice", "category": "Beverages"},
        {"name": "Orange Juice", "description": "Fresh orange juice", "category": "Beverages"},
        {"name": "Bread", "description": "Fresh bread", "category": "Bakery"}
    ]
    
    for product in products:
        client.post("/products/", json=product)
    
    # Search for juice products
    response = client.get("/products/?search=juice")
    assert response.status_code == 200
    
    data = response.json()
    assert data["success"] is True
    assert len(data["data"]) == 2
    assert all("juice" in product["name"].lower() for product in data["data"])

def test_pagination():
    """Test pagination functionality"""
    # Create multiple test products
    for i in range(15):
        product_data = {
            "name": f"Product {i}",
            "description": f"Description for product {i}",
            "category": "Test Category",
            "price": float(i + 1),
            "stock_quantity": i + 1
        }
        client.post("/products/", json=product_data)
    
    # Test first page
    response = client.get("/products/?skip=0&limit=5")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data["data"]) == 5
    assert data["total"] == 15
    assert data["page"] == 1
    assert data["size"] == 5
    
    # Test second page
    response = client.get("/products/?skip=5&limit=5")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data["data"]) == 5
    assert data["page"] == 2

def test_create_product_validation():
    """Test product creation validation"""
    # Test missing required field (name)
    product_data = {
        "description": "A product without name",
        "category": "Test",
        "price": 10.99
    }
    
    response = client.post("/products/", json=product_data)
    assert response.status_code == 422  # Validation error

def test_update_product_empty_data():
    """Test updating product with empty data"""
    # Create a test product first
    product_data = {
        "name": "Empty Update Test",
        "description": "A product for empty update test",
        "category": "Test",
        "price": 10.99
    }
    create_response = client.post("/products/", json=product_data)
    product_id = create_response.json()["data"]["id"]
    
    # Try to update with empty data
    response = client.put(f"/products/{product_id}", json={})
    assert response.status_code == 400
    assert response.json()["detail"] == "No update data provided"
