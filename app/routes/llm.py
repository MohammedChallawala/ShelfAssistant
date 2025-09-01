from fastapi import APIRouter, HTTPException, Form, Query
from ..models.response import DataResponse
from typing import Dict, Any, Optional
from ..services.llm import llm_service

router = APIRouter(prefix="/llm", tags=["llm"])

@router.get("/status", response_model=DataResponse[Dict[str, Any]])
async def get_llm_status():
    status = llm_service.get_service_status()
    return DataResponse(success=status.get("is_connected", False), message="LLM status", data=status)

@router.post("/ask", response_model=DataResponse[str])
async def ask_question(
    question: str = Form(..., description="User question"),
    search: Optional[str] = Form(None, description="Optional keyword to filter product context"),
    model: Optional[str] = Form(None, description="Override model name (e.g., phi, phi3:mini)")
):
    try:
        if model:
            llm_service.set_model(model)
        ctx = llm_service.build_product_context(search)
        answer = llm_service.generate_answer(question=question, context=ctx["context"]) 
        return DataResponse(success=True, message="OK", data=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
