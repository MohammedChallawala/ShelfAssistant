#!/usr/bin/env python3
"""
Simple system test for ShelfAssistant
Tests text queries, image uploads, and camera capture
"""
import requests
import time
import os
from pathlib import Path

BASE_URL = "http://localhost:8000"

def test_health():
    """Test if the API is running"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ API is running")
            return True
        else:
            print(f"❌ API returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to API: {e}")
        return False

def test_llm_status():
    """Test LLM service status"""
    try:
        response = requests.get(f"{BASE_URL}/llm/status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ LLM Status: {data['data']['status']}")
            print(f"   Text Model: {data['data']['text_model']}")
            print(f"   Vision Model: {data['data']['vision_model']}")
            return data['data']['is_connected']
        else:
            print(f"❌ LLM status failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ LLM status error: {e}")
        return False

def test_text_query():
    """Test text-only query"""
    try:
        response = requests.post(
            f"{BASE_URL}/llm/query",
            data={"question": "Hello, can you help me with product information?"},
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Text query successful: {data['data'][:100]}...")
            return True
        else:
            print(f"❌ Text query failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Text query error: {e}")
        return False

def test_image_upload():
    """Test image upload (if test image exists)"""
    # Look for a test image
    test_images = ["test_image.jpg", "shelf.jpg", "sample.jpg"]
    test_image = None
    
    for img in test_images:
        if os.path.exists(img):
            test_image = img
            break
    
    if not test_image:
        print("⚠️  No test image found. Skipping image upload test.")
        print("   Create a test image or use camera capture instead.")
        return True
    
    try:
        with open(test_image, 'rb') as f:
            files = {'image': f}
            response = requests.post(
                f"{BASE_URL}/llm/query",
                files=files,
                timeout=60
            )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Image upload successful: {data['data'][:100]}...")
            return True
        else:
            print(f"❌ Image upload failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Image upload error: {e}")
        return False

def test_camera_capture():
    """Test camera capture (may fail if no camera)"""
    try:
        response = requests.post(f"{BASE_URL}/vision/capture", timeout=60)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Camera capture successful: {data['data'][:100]}...")
            return True
        else:
            print(f"❌ Camera capture failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Camera capture error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 ShelfAssistant System Test")
    print("=" * 50)
    
    # Test 1: API Health
    if not test_health():
        print("\n❌ API is not running. Start it with:")
        print("   uvicorn app.main:app --reload --port 8000")
        return
    
    # Test 2: LLM Status
    llm_ok = test_llm_status()
    if not llm_ok:
        print("\n⚠️  LLM not connected. Make sure Ollama is running:")
        print("   ollama serve")
        print("   ollama pull phi3:mini")
        print("   ollama pull moondream")
    
    # Test 3: Text Query
    print("\n📝 Testing text query...")
    test_text_query()
    
    # Test 4: Image Upload
    print("\n📸 Testing image upload...")
    test_image_upload()
    
    # Test 5: Camera Capture
    print("\n📷 Testing camera capture...")
    test_camera_capture()
    
    print("\n🎉 Test completed!")
    print("\n💡 Next steps:")
    print("   1. Visit http://localhost:8000/docs for interactive testing")
    print("   2. Try uploading an image via the web interface")
    print("   3. Use curl commands for programmatic access")

if __name__ == "__main__":
    main()
