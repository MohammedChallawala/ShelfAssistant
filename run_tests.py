#!/usr/bin/env python3
"""
Simple test runner for ShelfAssistant API tests
"""
import subprocess
import sys
import os

def run_tests():
    """Run the test suite"""
    print("🧪 Running ShelfAssistant API tests...")
    
    # Check if pytest is available
    try:
        import pytest
    except ImportError:
        print("❌ pytest not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pytest", "httpx"])
    
    # Run tests
    test_dir = "tests"
    if not os.path.exists(test_dir):
        print(f"❌ Test directory '{test_dir}' not found")
        return False
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            test_dir, 
            "-v", 
            "--tb=short"
        ], capture_output=False)
        
        if result.returncode == 0:
            print("✅ All tests passed!")
            return True
        else:
            print("❌ Some tests failed!")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running tests: {e}")
        return False

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
