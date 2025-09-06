# Speech-to-Text service using faster-whisper with fallback
import os
from typing import Optional
from pathlib import Path

try:
    from faster_whisper import WhisperModel
    FASTER_WHISPER_AVAILABLE = True
except ImportError as e:
    print(f"faster-whisper import failed: {e}")
    FASTER_WHISPER_AVAILABLE = False

# Fallback: Try to use OpenAI Whisper API or other alternatives
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

class STTService:
    """Speech-to-Text service using faster-whisper with fallback options."""
    
    def __init__(self, model_size: str = "tiny", device: str = "cpu"):
        self.model_size = model_size
        self.device = device
        self.model = None
        self.is_initialized = False
        self.fallback_mode = False
    
    def initialize_model(self):
        """Initialize the Whisper model with fallback options."""
        if not FASTER_WHISPER_AVAILABLE:
            print("⚠️  faster-whisper not available. Using fallback mode.")
            self.fallback_mode = True
            self.is_initialized = True
            return
        
        if not self.is_initialized:
            try:
                print(f"Loading Whisper model: {self.model_size} on {self.device}")
                # Try to initialize without av dependency
                self.model = WhisperModel(
                    self.model_size, 
                    device=self.device,
                    compute_type="int8" if self.device == "cpu" else "float16"
                )
                self.is_initialized = True
                print("Whisper model loaded successfully")
            except Exception as e:
                print(f"⚠️  Failed to load faster-whisper: {e}")
                print("Using fallback mode.")
                self.fallback_mode = True
                self.is_initialized = True
    
    def transcribe_audio(self, audio_path: str) -> str:
        """Transcribe audio file to text using faster-whisper or fallback.
        
        Args:
            audio_path: Path to the audio file
            
        Returns:
            Transcribed text string
        """
        if not self.is_initialized:
            self.initialize_model()
        
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        # If in fallback mode, return a placeholder
        if self.fallback_mode:
            return "[STT Fallback] Audio transcription not available. Please install faster-whisper or use text input instead."
        
        try:
            # Transcribe with faster-whisper
            segments, info = self.model.transcribe(
                audio_path,
                beam_size=5,
                language="en",  # Set to None for auto-detection
                condition_on_previous_text=False
            )
            
            # Combine all segments into a single transcript
            transcript = ""
            for segment in segments:
                transcript += segment.text.strip() + " "
            
            return transcript.strip()
            
        except Exception as e:
            raise RuntimeError(f"Transcription failed: {str(e)}")
    
    def get_model_info(self) -> dict:
        """Get information about the STT service."""
        return {
            "service_name": "faster-whisper" if not self.fallback_mode else "fallback",
            "model_size": self.model_size,
            "device": self.device,
            "is_initialized": self.is_initialized,
            "available": FASTER_WHISPER_AVAILABLE,
            "fallback_mode": self.fallback_mode
        }

# Global STT service instance
stt_service = STTService()
