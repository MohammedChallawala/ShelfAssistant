#!/usr/bin/env python3
"""
Test script for the vision module
"""
import sys
import os
sys.path.append('.')

from app.vision import detect, _YOLO_AVAILABLE

def test_vision():
    print("Testing Vision Module...")
    print(f"YOLO Available: {_YOLO_AVAILABLE}")
    
    # Test dummy detection
    print("\nTesting dummy detection:")
    dummy_result = detect("C:\Users\moham\OneDrive\Desktop\sample image.png")
    print(f"Dummy result: {dummy_result}")
    
    if _YOLO_AVAILABLE:
        print("\nYOLO is available! Testing with a sample image...")
        # Check if we have any test images
        test_images = []
        for ext in ['.jpg', '.jpeg', '.png', '.bmp']:
            for root, dirs, files in os.walk('.'):
                for file in files:
                    if file.lower().endswith(ext):
                        test_images.append(os.path.join(root, file))
        
        if test_images:
            print(f"Found test images: {test_images[:3]}")  # Show first 3
            # Test with first image
            try:
                result = detect(test_images[0])
                print(f"YOLO detection result: {result}")
            except Exception as e:
                print(f"Error testing YOLO: {e}")
        else:
            print("No test images found. You can add images to test YOLO detection.")
    else:
        print("\nYOLO not available - using dummy detection only")
    
    print("\nVision module test completed!")

if __name__ == "__main__":
    test_vision()
