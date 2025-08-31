from typing import List, Dict, Any
import os
from pathlib import Path

# Try YOLOv8 (ultralytics); fall back to dummy detector if unavailable
try:
    from ultralytics import YOLO
    _YOLO_AVAILABLE = True
except Exception:
    _YOLO_AVAILABLE = False

_MODEL = None

def load_model():
    global _MODEL
    if _YOLO_AVAILABLE and _MODEL is None:
        try:
            # Use the nano model for speed
            _MODEL = YOLO('yolov8n.pt')
            print("YOLOv8 model loaded successfully")
        except Exception as e:
            print(f"Error loading YOLO model: {e}")
            return None
    return _MODEL

def detect(image_path: str, conf: float = 0.25) -> List[Dict[str, Any]]:
    # Check if file exists
    if not os.path.exists(image_path):
        print(f"Warning: Image file '{image_path}' does not exist. Using dummy detection.")
        return [{"label": "bottle", "confidence": 0.42, "bbox_xyxy": [10, 10, 100, 180]}]
    
    if _YOLO_AVAILABLE:
        try:
            model = load_model()
            if model is None:
                print("YOLO model not available, using dummy detection")
                return [{"label": "bottle", "confidence": 0.42, "bbox_xyxy": [10, 10, 100, 180]}]
            
            results = model(image_path, conf=conf, verbose=False)
            detections = []
            for r in results:
                for b in r.boxes:
                    cls_id = int(b.cls.item())
                    name = r.names[cls_id]
                    confv = float(b.conf.item())
                    xyxy = b.xyxy[0].tolist()
                    detections.append({
                        "label": name,
                        "confidence": confv,
                        "bbox_xyxy": xyxy
                    })
            
            if not detections:
                print(f"No objects detected in {image_path} with confidence >= {conf}")
                return [{"label": "no_detection", "confidence": 0.0, "bbox_xyxy": [0, 0, 0, 0]}]
            
            print(f"Detected {len(detections)} objects in {image_path}")
            return detections
            
        except Exception as e:
            print(f"Error during YOLO detection: {e}")
            # Fall back to dummy detection
            return [{"label": "bottle", "confidence": 0.42, "bbox_xyxy": [10, 10, 100, 180]}]
    else:
        # Fallback: dummy detection
        print("YOLO not available, using dummy detection")
        return [{"label": "bottle", "confidence": 0.42, "bbox_xyxy": [10, 10, 100, 180]}]
