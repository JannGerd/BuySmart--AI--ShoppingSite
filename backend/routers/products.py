from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from backend import models, schemas, database
from backend.security import get_current_user
from typing import List, Optional
import logging

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

logger = logging.getLogger(__name__)

# ==================================================
# Database Dependency
# ==================================================
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==================================================
# Create Product (Requires Authentication)
# ==================================================
@router.post("/", response_model=schemas.ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
) -> schemas.ProductOut:
    """
    Create a new product (requires authentication).
    """
    try:
        new_product = models.Product(**product.dict())
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        logger.info(f"Product created successfully. ID: {new_product.product_id}")
        return new_product
    except Exception as e:
        logger.exception(f"Error creating product: {e}")
        raise HTTPException(status_code=500, detail="Error creating product.")


# ==================================================
# Retrieve All Products (Public)
# ==================================================
@router.get("/", response_model=List[schemas.ProductOut], status_code=status.HTTP_200_OK)
def get_all_products(db: Session = Depends(get_db)) -> List[schemas.ProductOut]:
    """
    Retrieve all available products.
    """
    try:
        products = db.query(models.Product).all()
        if not products:
            logger.warning("No products found in the database.")
        else:
            logger.info(f"{len(products)} products retrieved successfully.")
        return products
    except Exception as e:
        logger.exception(f"Error retrieving products: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving products.")


# ==================================================
# Retrieve Product by ID (Public)
# ==================================================
@router.get("/{product_id}", response_model=schemas.ProductOut, status_code=status.HTTP_200_OK)
def get_product(product_id: int, db: Session = Depends(get_db)) -> schemas.ProductOut:
    """
    Retrieve a specific product by its ID.
    """
    try:
        product = db.query(models.Product).filter(models.Product.product_id == product_id).first()
        if not product:
            logger.error(f"Product not found. ID: {product_id}")
            raise HTTPException(status_code=404, detail="Product not found.")
        logger.info(f"Product retrieved successfully. ID: {product_id}")
        return product
    except Exception as e:
        logger.exception(f"Error retrieving product {product_id}: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving product.")


# ==================================================
# Update Product (Requires Authentication)
# ==================================================
@router.put("/{product_id}", response_model=schemas.ProductOut, status_code=status.HTTP_200_OK)
def update_product(
    product_id: int,
    updated_product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
) -> schemas.ProductOut:
    """
    Update an existing product by its ID (requires authentication).
    """
    try:
        product = db.query(models.Product).filter(models.Product.product_id == product_id).first()
        if not product:
            logger.error(f"Product not found for update. ID: {product_id}")
            raise HTTPException(status_code=404, detail="Product not found.")

        for key, value in updated_product.dict().items():
            setattr(product, key, value)

        db.commit()
        db.refresh(product)
        logger.info(f"Product updated successfully. ID: {product_id}")
        return product
    except Exception as e:
        logger.exception(f"Error updating product {product_id}: {e}")
        raise HTTPException(status_code=500, detail="Error updating product.")


# ==================================================
# Delete Product (Requires Authentication)
# ==================================================
@router.delete("/{product_id}", status_code=status.HTTP_200_OK)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
) -> dict:
    """
    Delete a product by its ID (requires authentication).
    """
    try:
        product = db.query(models.Product).filter(models.Product.product_id == product_id).first()
        if not product:
            logger.error(f"Product not found for deletion. ID: {product_id}")
            raise HTTPException(status_code=404, detail="Product not found.")

        db.delete(product)
        db.commit()
        logger.info(f"Product deleted successfully. ID: {product_id}")
        return {"message": "Product deleted successfully."}
    except Exception as e:
        logger.exception(f"Error deleting product {product_id}: {e}")
        raise HTTPException(status_code=500, detail="Error deleting product.")


# ==================================================
# Search Products (Public)
# ==================================================
@router.get("/search/", response_model=List[schemas.ProductOut], status_code=status.HTTP_200_OK)
def search_products(
    name: Optional[str] = Query(None, description="Partial or full product name"),
    min_price: Optional[float] = Query(None, description="Minimum price filter"),
    max_price: Optional[float] = Query(None, description="Maximum price filter"),
    min_stock: Optional[int] = Query(None, description="Minimum stock quantity"),
    max_stock: Optional[int] = Query(None, description="Maximum stock quantity"),
    db: Session = Depends(get_db)
) -> List[schemas.ProductOut]:
    """
    Search for products by name, price range, and stock quantity.
    Supports partial matches and numeric filtering.
    """
    try:
        query = db.query(models.Product)

        if name:
            query = query.filter(models.Product.product_name.ilike(f"%{name}%"))
        if min_price is not None:
            query = query.filter(models.Product.product_price >= min_price)
        if max_price is not None:
            query = query.filter(models.Product.product_price <= max_price)
        if min_stock is not None:
            query = query.filter(models.Product.stock_quantity >= min_stock)
        if max_stock is not None:
            query = query.filter(models.Product.stock_quantity <= max_stock)

        products = query.all()

        if not products:
            logger.warning("No products found matching the given filters.")
            raise HTTPException(status_code=404, detail="No products match the search criteria.")

        logger.info(f"Search returned {len(products)} products.")
        return products
    except Exception as e:
        logger.exception(f"Error searching products: {e}")
        raise HTTPException(status_code=500, detail="Error searching products.")
