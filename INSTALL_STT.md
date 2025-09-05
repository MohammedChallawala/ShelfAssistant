# Speech-to-Text Installation Guide

## Current Status
The system is currently running in **fallback mode** because `faster-whisper` requires compilation on Windows.

## Option 1: Use Fallback Mode (Current)
The system works with a fallback message for audio transcription. You can still use:
- Text queries
- Image analysis
- All other features

## Option 2: Install faster-whisper (Recommended for full functionality)

### For Windows:
1. **Install Microsoft Visual C++ Build Tools:**
   - Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
   - Install "C++ build tools" workload
   - Restart your computer

2. **Install faster-whisper:**
   ```bash
   pip install faster-whisper==1.0.3
   ```

3. **Restart the API:**
   ```bash
   uvicorn app.main:app --reload
   ```

### For Linux/macOS:
```bash
pip install faster-whisper==1.0.3
```

## Option 3: Use Pre-compiled Wheels
If you have issues with compilation, try:
```bash
pip install --only-binary=all faster-whisper==1.0.3
```

## Testing
After installation, test with:
```bash
python test_voice.py
```

## Alternative STT Solutions
If faster-whisper continues to have issues, you can modify `app/services/stt.py` to use:
- OpenAI Whisper API
- Google Speech-to-Text
- Azure Speech Services
- Other cloud-based STT services

## Current Fallback Behavior
- Audio uploads return: `[STT Fallback] Audio transcription not available...`
- Text queries work normally
- Image analysis works normally
- All other features function as expected

