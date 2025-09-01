from typing import Optional, Tuple
from pathlib import Path
import time
import tempfile

# Prefer Picamera2; fallback to OpenCV for non-RPi environments
try:
    from picamera2 import Picamera2  # type: ignore
    PICAMERA_AVAILABLE = True
except Exception:
    PICAMERA_AVAILABLE = False

try:
    import cv2  # type: ignore
    OPENCV_AVAILABLE = True
except Exception:
    OPENCV_AVAILABLE = False

class ImageHandler:
    """Image capture and IO utilities with modular backends.

    This class abstracts camera capture using Picamera2 (preferred on RPi)
    or OpenCV fallback. It also manages temporary files for downstream
    processing pipelines (e.g., LLM multimodal inference, detection).
    """

    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = Path(output_dir) if output_dir else Path(tempfile.gettempdir())
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.camera_initialized = False
        self.backend = None  # 'picamera2' or 'opencv'

    def initialize_camera(self, prefer_picamera: bool = True) -> None:
        if prefer_picamera and PICAMERA_AVAILABLE:
            self.backend = 'picamera2'
            self.camera_initialized = True
            return
        if OPENCV_AVAILABLE:
            self.backend = 'opencv'
            self.camera_initialized = True
            return
        raise RuntimeError("No supported camera backend available (Picamera2 or OpenCV required)")

    def capture_image(self, filename_prefix: str = "capture", prefer_picamera: bool = True) -> Path:
        if not self.camera_initialized:
            self.initialize_camera(prefer_picamera=prefer_picamera)

        timestamp = int(time.time() * 1000)
        out_path = self.output_dir / f"{filename_prefix}_{timestamp}.jpg"

        if self.backend == 'picamera2':
            # Minimal Picamera2 capture path (no preview)
            cam = Picamera2()
            config = cam.create_still_configuration()
            cam.configure(config)
            cam.start()
            time.sleep(0.2)
            cam.capture_file(str(out_path))
            cam.stop()
            cam.close()
            return out_path

        if self.backend == 'opencv':
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                cap.release()
                raise RuntimeError("OpenCV could not open camera index 0")
            ret, frame = cap.read()
            cap.release()
            if not ret:
                raise RuntimeError("OpenCV failed to read frame from camera")
            cv2.imwrite(str(out_path), frame)
            return out_path

        raise RuntimeError("Camera backend not initialized correctly")

    def save_uploaded_image(self, data: bytes, filename_prefix: str = "upload") -> Path:
        timestamp = int(time.time() * 1000)
        out_path = self.output_dir / f"{filename_prefix}_{timestamp}.jpg"
        with open(out_path, 'wb') as f:
            f.write(data)
        return out_path

# Global instance
image_handler = ImageHandler()
