#!/usr/bin/env python3
"""
Demo script for ShelfAssistant Products API
This script demonstrates the CRUD operations for products
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def print_response(response, operation):
    """Print formatted API response"""
    print(f"\n🔹 {operation}")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Success: {data.get('success')}")
        print(f"Message: {data.get('message')}")
        if data.get('data'):
            print(f"Data: {json.dumps(data['data'], indent=2)}")
    else:
        print(f"Error: {response.text}")
    print("-" * 50)

def demo_products_api():
    """Demonstrate products API functionality"""
    print("🛒 ShelfAssistant Products API Demo")
    print("=" * 50)
    
    # Wait for API to be ready
    print("⏳ Waiting for API to be ready...")
    max_retries = 10
    for i in range(max_retries):
        try:
            response = requests.get(f"{BASE_URL}/health")
            if response.status_code == 200:
                print("✅ API is ready!")
                break
        except requests.exceptions.ConnectionError:
            if i < max_retries - 1:
                print(f"⏳ Retrying... ({i+1}/{max_retries})")
                time.sleep(1)
            else:
                print("❌ Could not connect to API. Make sure it's running with:")
                print("   uvicorn app.main:app --reload --port 8000")
                return
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return
    
    # 1. Create a product
    print("\n📝 Creating a new product...")
    product_data = {
        "name": "Organic Apple Juice",
        "description": "Fresh organic apple juice, 100% natural",
        "category": "Beverages",
        "price": 4.99,
        "stock_quantity": 25,
        "shelf_location": "A1-B3",
        "barcode": "1234567890123"
    }
    
    response = requests.post(f"{BASE_URL}/products/", json=product_data)
    print_response(response, "CREATE Product")
    
    if response.status_code != 200:
        print("❌ Failed to create product. Stopping demo.")
        return
    
    product_id = response.json()["data"]["id"]
    
    # 2. Get all products
    print("\n📋 Getting all products...")
    response = requests.get(f"{BASE_URL}/products/")
    print_response(response, "GET All Products")
    
    # 3. Get specific product
    print(f"\n🔍 Getting product with ID {product_id}...")
    response = requests.get(f"{BASE_URL}/products/{product_id}")
    print_response(response, "GET Product by ID")
    
    # 4. Update product
    print(f"\n✏️ Updating product {product_id}...")
    update_data = {
        "price": 5.49,
        "stock_quantity": 20,
        "description": "Fresh organic apple juice, 100% natural, now with enhanced flavor"
    }
    
    response = requests.put(f"{BASE_URL}/products/{product_id}", json=update_data)
    print_response(response, "UPDATE Product")
    
    # 5. Search products
    print("\n🔍 Searching for 'juice' products...")
    response = requests.get(f"{BASE_URL}/products/?search=juice")
    print_response(response, "SEARCH Products")
    
    # 6. Test pagination
    print("\n📄 Testing pagination...")
    response = requests.get(f"{BASE_URL}/products/?skip=0&limit=5")
    print_response(response, "PAGINATION Test")
    
    # 7. Create another product for variety
    print("\n📝 Creating another product...")
    product_data_2 = {
        "name": "Whole Grain Bread",
        "description": "Fresh whole grain bread, baked daily",
        "category": "Bakery",
        "price": 3.99,
        "stock_quantity": 15,
        "shelf_location": "C2-D1",
        "barcode": "9876543210987"
    }
    
    response = requests.post(f"{BASE_URL}/products/", json=product_data_2)
    print_response(response, "CREATE Second Product")
    
    # 8. Get all products again
    print("\n📋 Getting all products after adding second product...")
    response = requests.get(f"{BASE_URL}/products/")
    print_response(response, "GET All Products (Updated)")
    
    # 9. Delete the first product
    print(f"\n🗑️ Deleting product {product_id}...")
    response = requests.delete(f"{BASE_URL}/products/{product_id}")
    print_response(response, "DELETE Product")
    
    # 10. Verify deletion
    print(f"\n🔍 Verifying product {product_id} was deleted...")
    response = requests.get(f"{BASE_URL}/products/{product_id}")
    print_response(response, "VERIFY Deletion")
    
    print("\n🎉 Demo completed!")
    print("\n💡 Try the interactive API docs at:")
    print(f"   {BASE_URL}/docs")

if __name__ == "__main__":
    try:
        demo_products_api()
    except KeyboardInterrupt:
        print("\n\n⏹️ Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        print("\n💡 Make sure the API is running with:")
        print("   uvicorn app.main:app --reload --port 8000")
