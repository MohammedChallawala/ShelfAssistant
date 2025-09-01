from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ProductBase(BaseModel):
    name: str = Field(..., description="Product name")
    description: Optional[str] = Field(None, description="Product description")
    category: Optional[str] = Field(None, description="Product category")
    price: Optional[float] = Field(None, description="Product price")
    stock_quantity: int = Field(default=0, description="Current stock quantity")
    shelf_location: Optional[str] = Field(None, description="Shelf location identifier")
    barcode: Optional[str] = Field(None, description="Product barcode")

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    stock_quantity: Optional[int] = None
    shelf_location: Optional[str] = None
    barcode: Optional[str] = None

class Product(ProductBase):
    id: int = Field(..., description="Product ID")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")

    class Config:
        from_attributes = True
