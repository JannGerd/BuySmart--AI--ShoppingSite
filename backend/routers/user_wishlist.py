from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend import models, schemas, database
from backend.security import get_current_user
from typing import List
import logging

router = APIRouter(
    prefix="/wishlist",
    tags=["Wishlist"]
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
# Add Item to Wishlist (Requires Authentication)
# ==================================================
@router.post("/", response_model=schemas.UserWishlistOut, status_code=status.HTTP_201_CREATED)
def add_to_wishlist(
    item: schemas.UserWishlistCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
) -> schemas.UserWishlistOut:
    """
    Add a new item to the current user's wishlist.
    """
    try:
        wishlist_item = models.UserWishlist(**item.dict())
        db.add(wishlist_item)
        db.commit()
        db.refresh(wishlist_item)
        logger.info(f"Wishlist item added successfully. ID: {wishlist_item.id}, User: {wishlist_item.user_id}")
        return wishlist_item
    except Exception as e:
        logger.exception(f"Error adding item to wishlist: {e}")
        raise HTTPException(status_code=500, detail="Error adding item to wishlist.")


# ==================================================
# Get User Wishlist (Requires Authentication)
# ==================================================
@router.get("/", response_model=List[schemas.UserWishlistOut], status_code=status.HTTP_200_OK)
def get_user_wishlist(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
) -> List[schemas.UserWishlistOut]:
    """
    Retrieve all items in the current user's wishlist.
    """
    try:
        wishlist = db.query(models.UserWishlist).filter(models.UserWishlist.user_id == current_user.id).all()
        if not wishlist:
            logger.warning(f"No wishlist items found for user ID: {current_user.id}")
        else:
            logger.info(f"{len(wishlist)} wishlist items retrieved for user ID: {current_user.id}")
        return wishlist
    except Exception as e:
        logger.exception(f"Error retrieving wishlist for user ID {current_user.id}: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving wishlist.")


# ==================================================
# Delete Item from Wishlist (Requires Authentication)
# ==================================================
@router.delete("/{item_id}", status_code=status.HTTP_200_OK)
def delete_from_wishlist(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
) -> dict:
    """
    Delete an item from the current user's wishlist.
    """
    try:
        item = db.query(models.UserWishlist).filter(
            models.UserWishlist.id == item_id,
            models.UserWishlist.user_id == current_user.id
        ).first()

        if not item:
            logger.error(f"Wishlist item not found or not owned by user. ID: {item_id}")
            raise HTTPException(status_code=404, detail="Wishlist item not found.")

        db.delete(item)
        db.commit()
        logger.info(f"Wishlist item deleted successfully. ID: {item_id}, User: {current_user.id}")
        return {"message": "Item successfully removed from wishlist."}
    except Exception as e:
        logger.exception(f"Error deleting wishlist item {item_id}: {e}")
        raise HTTPException(status_code=500, detail="Error deleting wishlist item.")
