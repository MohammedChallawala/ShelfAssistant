#!/usr/bin/env python3
"""
Test script for voice functionality
"""
import requests
import time
import os

BASE_URL = "http://localhost:8000"

def test_stt_status():
    """Test STT service status"""
    try:
        response = requests.get(f"{BASE_URL}/llm/stt/status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ STT Service Status:")
            print(f"   Service: {data['data']['service_name']}")
            print(f"   Model Size: {data['data']['model_size']}")
            print(f"   Available: {data['data']['available']}")
            print(f"   Initialized: {data['data']['is_initialized']}")
            return True
        else:
            print(f"❌ STT status failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ STT status error: {e}")
        return False

def test_voice_endpoint():
    """Test voice endpoint with a dummy audio file"""
    # Create a simple test audio file (silence)
    test_audio_path = "test_audio.wav"
    
    # For testing, we'll create a minimal WAV file
    # In real usage, this would be a recorded audio file
    try:
        # Create a minimal WAV file header (1 second of silence)
        wav_data = b'RIFF$\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x44\xac\x00\x00\x88X\x01\x00\x02\x00\x10\x00data\x00\x00\x00\x00'
        
        with open(test_audio_path, 'wb') as f:
            f.write(wav_data)
        
        # Test the voice endpoint
        with open(test_audio_path, 'rb') as f:
            files = {'audio': ('test.wav', f, 'audio/wav')}
            response = requests.post(f"{BASE_URL}/llm/voice", files=files, timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Voice endpoint test successful")
            print(f"   Transcript: {data['data']['transcript']}")
            print(f"   Response: {data['data']['response']}")
            return True
        else:
            print(f"❌ Voice endpoint failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Voice endpoint error: {e}")
        return False
    finally:
        # Clean up test file
        if os.path.exists(test_audio_path):
            os.remove(test_audio_path)

def main():
    """Run voice functionality tests"""
    print("🎤 Voice Functionality Test")
    print("=" * 40)
    
    # Test 1: STT Status
    print("\n1. Testing STT service status...")
    test_stt_status()
    
    # Test 2: Voice Endpoint
    print("\n2. Testing voice endpoint...")
    test_voice_endpoint()
    
    print("\n💡 To test with real audio:")
    print("   1. Start the API: uvicorn app.main:app --reload")
    print("   2. Start Gradio UI: python ui/gradio_app.py")
    print("   3. Go to http://localhost:7860 and use the Voice tab")
    print("   4. Record a question and click 'Process Voice Query'")

if __name__ == "__main__":
    main()

