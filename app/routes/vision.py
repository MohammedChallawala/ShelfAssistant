from fastapi import APIRouter, HTTPException, UploadFile, File
from ..models.response import DataResponse
from typing import List, Dict, Any

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
