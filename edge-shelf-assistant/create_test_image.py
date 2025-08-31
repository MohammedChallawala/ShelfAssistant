#!/usr/bin/env python3
"""
Create a simple test image for testing the vision module
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_test_image():
    # Create a simple test image with some shapes that might be detected
    width, height = 640, 480
    image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(image)
    
    # Draw some simple shapes that might be detected by YOLO
    # Rectangle (could be detected as a bottle or box)
    draw.rectangle([100, 100, 200, 300], fill='blue', outline='black', width=2)
    
    # Circle (could be detected as a ball or fruit)
    draw.ellipse([300, 150, 400, 250], fill='red', outline='black', width=2)
    
    # Another rectangle (could be detected as a book or device)
    draw.rectangle([450, 200, 550, 350], fill='green', outline='black', width=2)
    
    # Add some text
    try:
        # Try to use a default font
        font = ImageFont.load_default()
    except:
        font = None
    
    draw.text((50, 50), "Test Image for Vision Module", fill='black', font=font)
    draw.text((50, 400), "Blue rectangle, Red circle, Green rectangle", fill='black', font=font)
    
    # Save the image
    test_image_path = "test_image.jpg"
    image.save(test_image_path, "JPEG", quality=95)
    print(f"Test image created: {test_image_path}")
    print(f"Image size: {width}x{height}")
    print(f"File size: {os.path.getsize(test_image_path)} bytes")
    
    return test_image_path

if __name__ == "__main__":
    create_test_image()
