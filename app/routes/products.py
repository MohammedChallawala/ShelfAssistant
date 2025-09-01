from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from ..models.product import Product, ProductCreate, ProductUpdate
from ..models.response import DataResponse, ListResponse
from ..services.db import db_service

router = APIRouter(prefix="/products", tags=["products"])

@router.post("/", response_model=DataResponse[Product])
async def create_product(product: ProductCreate):
    """Create a new product"""
    try:
        product_data = product.model_dump()
        product_id = db_service.create_product(product_data)
        
        # Get the created product
        created_product = db_service.get_product(product_id)
        if not created_product:
            raise HTTPException(status_code=500, detail="Failed to retrieve created product")
        
        return DataResponse(
            success=True,
            message="Product created successfully",
            data=Product(**created_product)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create product: {str(e)}")

@router.get("/", response_model=ListResponse[Product])
async def get_products(
    skip: int = Query(0, ge=0, description="Number of products to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of products to return"),
    search: Optional[str] = Query(None, description="Search query for product name, description, or category")
):
    """Get all products with optional pagination and search"""
    try:
        if search:
            products = db_service.search_products(search)
        else:
            products = db_service.get_all_products()
        
        # Apply pagination
        total = len(products)
        paginated_products = products[skip:skip + limit]
        
        return ListResponse(
            success=True,
            message="Products retrieved successfully",
            data=[Product(**product) for product in paginated_products],
            total=total,
            page=skip // limit + 1 if limit > 0 else 1,
            size=limit
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve products: {str(e)}")

@router.get("/{product_id}", response_model=DataResponse[Product])
async def get_product(product_id: int):
    """Get a specific product by ID"""
    try:
        product = db_service.get_product(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return DataResponse(
            success=True,
            message="Product retrieved successfully",
            data=Product(**product)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve product: {str(e)}")

@router.put("/{product_id}", response_model=DataResponse[Product])
async def update_product(product_id: int, product_update: ProductUpdate):
    """Update a product by ID"""
    try:
        # Check if product exists
        existing_product = db_service.get_product(product_id)
        if not existing_product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Update the product
        update_data = product_update.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=400, detail="No update data provided")
        
        success = db_service.update_product(product_id, update_data)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to update product")
        
        # Get the updated product
        updated_product = db_service.get_product(product_id)
        if not updated_product:
            raise HTTPException(status_code=500, detail="Failed to retrieve updated product")
        
        return DataResponse(
            success=True,
            message="Product updated successfully",
            data=Product(**updated_product)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update product: {str(e)}")

@router.delete("/{product_id}")
async def delete_product(product_id: int):
    """Delete a product by ID"""
    try:
        # Check if product exists
        existing_product = db_service.get_product(product_id)
        if not existing_product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Delete the product
        success = db_service.delete_product(product_id)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to delete product")
        
        return DataResponse(
            success=True,
            message="Product deleted successfully",
            data=None
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete product: {str(e)}")
