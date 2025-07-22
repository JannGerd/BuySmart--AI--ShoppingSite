from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend import models, schemas, database

router = APIRouter(
    prefix="/wishlist",
    tags=["wishlist"]
)

@router.post("/", response_model=schemas.UserWishlist)
def create_wishlist_item(wishlist: schemas.UserWishlistCreate, db: Session = Depends(get_db)):
    db_wishlist = models.UserWishlist(**wishlist.dict())
    db.add(db_wishlist)
    db.commit()
    db.refresh(db_wishlist)
    return db_wishlist

@router.get("/", response_model=list[schemas.UserWishlist])
def read_all_wishlist_items(db: Session = Depends(get_db)):
    return db.query(models.UserWishlist).all()

@router.delete("/{wishlist_id}")
def delete_wishlist_item(wishlist_id: int, db: Session = Depends(get_db)):
    wishlist_item = db.query(models.UserWishlist).filter(models.UserWishlist.wishlist_id == wishlist_id).first()
    if wishlist_item is None:
        raise HTTPException(status_code=404, detail="Wishlist item not found")
    db.delete(wishlist_item)
    db.commit()
    return {"message": "Wishlist item deleted successfully"}


@router.put("/{wishlist_id}", response_model=schemas.UserWishlist)
def update_wishlist_item(
        wishlist_id: int,
        wishlist_update: schemas.UserWishlistCreate,  # את יכולה גם ליצור Schema חדש לעדכון אם תרצי
        db: Session = Depends(get_db)
):
    wishlist_item = db.query(models.UserWishlist).filter(models.UserWishlist.wishlist_id == wishlist_id).first()

    if wishlist_item is None:
        raise HTTPException(status_code=404, detail="Wishlist item not found")

    for key, value in wishlist_update.dict().items():
        setattr(wishlist_item, key, value)

    db.commit()
    db.refresh(wishlist_item)
    return wishlist_item
