from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from ..models.response import DataResponse
from typing import List, Dict, Any, Optional
from ..services.image_handler import image_handler
from ..services.llm import llm_service

router = APIRouter(prefix="/vision", tags=["vision"])

@router.post("/detect", response_model=DataResponse[List[Dict[str, Any]]])
async def detect_products(file: UploadFile = File(...)):
    """
    TODO: Implement YOLOv8 shelf recognition
    This endpoint will:
    1. Process uploaded shelf images
    2. Use YOLOv8 model for product detection
    3. Return detected products with confidence scores
    4. Map detections to product database
    """
    raise HTTPException(
        status_code=501, 
        detail="Vision endpoint not yet implemented. TODO: Integrate YOLOv8 detection"
    )

@router.get("/models", response_model=DataResponse[List[str]])
async def get_available_models():
    """
    TODO: Return available YOLOv8 models
    """
    raise HTTPException(
        status_code=501,
        detail="Model listing not yet implemented"
    )

@router.post("/capture", response_model=DataResponse[str])
async def capture_and_caption(
    user_query: Optional[str] = Form(None, description="Query about the captured image")
):
    """Capture an image from the camera and return a text caption via LLM.
    Uses moondream for vision analysis and phi3:mini for refinement.
    """
    try:
        img_path = image_handler.capture_image(filename_prefix="capture", prefer_picamera=True)
        
        # Use two-stage pipeline if user_query provided, otherwise simple caption
        if user_query:
            result = llm_service.image_to_text(str(img_path), user_query)
        else:
            result = llm_service.caption_image(str(img_path))
        
        return DataResponse(success=True, message="captured", data=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
