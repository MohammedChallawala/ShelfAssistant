from fastapi import APIRouter, HTTPException, Form, Query, UploadFile, File
from ..models.response import DataResponse
from typing import Dict, Any, Optional
from ..services.llm import llm_service
from ..services.image_handler import image_handler

router = APIRouter(prefix="/llm", tags=["llm"])

@router.get("/status", response_model=DataResponse[Dict[str, Any]])
async def get_llm_status():
    status = llm_service.get_service_status()
    return DataResponse(success=status.get("is_connected", False), message="LLM status", data=status)

@router.post("/ask", response_model=DataResponse[str])
async def ask_question(
    question: str = Form(..., description="User question"),
    search: Optional[str] = Form(None, description="Optional keyword to filter product context"),
    model: Optional[str] = Form(None, description="Override text model name (e.g., phi3:mini)")
):
    try:
        if model:
            llm_service.set_text_model(model)
        ctx = llm_service.build_product_context(search)
        answer = llm_service.generate_answer(question=question, context=ctx["context"]) 
        return DataResponse(success=True, message="OK", data=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/query", response_model=DataResponse[str])
async def unified_query(
    # Text mode
    question: Optional[str] = Form(None, description="Text question"),
    search: Optional[str] = Form(None, description="Optional keyword to filter product context"),
    # Image mode
    image: Optional[UploadFile] = File(None, description="Image to analyze"),
    user_query: Optional[str] = Form(None, description="Query about the image"),
    text_model: Optional[str] = Form(None, description="Override text model (e.g., phi3:mini)"),
    vision_model: Optional[str] = Form(None, description="Override vision model (e.g., moondream)")
):
    try:
        if text_model:
            llm_service.set_text_model(text_model)
        if vision_model:
            llm_service.set_vision_model(vision_model)

        # Auto-detect: image takes precedence if provided
        if image is not None:
            # Save uploaded image to temp and analyze
            bytes_data = await image.read()
            img_path = image_handler.save_uploaded_image(bytes_data, filename_prefix="query")
            
            # Use two-stage pipeline if user_query provided, otherwise simple caption
            if user_query:
                result = llm_service.image_to_text(str(img_path), user_query)
            else:
                result = llm_service.caption_image(str(img_path))
            
            return DataResponse(success=True, message="image", data=result)

        # Otherwise treat as text
        if not question:
            raise HTTPException(status_code=400, detail="Provide either 'image' or 'question'")
        ctx = llm_service.build_product_context(search)
        answer = llm_service.generate_answer(question=question, context=ctx["context"]) 
        return DataResponse(success=True, message="text", data=answer)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
