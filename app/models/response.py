from pydantic import BaseModel
from typing import Generic, TypeVar, Optional, List

T = TypeVar('T')

class ResponseBase(BaseModel):
    success: bool
    message: str

class DataResponse(ResponseBase, Generic[T]):
    data: T

class ListResponse(ResponseBase, Generic[T]):
    data: List[T]
    total: int
    page: Optional[int] = None
    size: Optional[int] = None

class ErrorResponse(ResponseBase):
    error_code: Optional[str] = None
    details: Optional[str] = None
