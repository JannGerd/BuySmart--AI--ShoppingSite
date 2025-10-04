from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend import models, schemas, database
from backend.security import get_current_user
from datetime import datetime
from typing import List
import logging

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

logger = logging.getLogger(__name__)

# ==========================================================
# Database Dependency
# ==========================================================
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==========================================================
# Create Order (Requires Authentication)
# ==========================================================
@router.post("/", response_model=schemas.Order, status_code=status.HTTP_201_CREATED)
def create_order(
    order: schemas.OrderCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
) -> schemas.Order:
    """Create a new order for the current user."""
    try:
        new_order = models.Order(**order.dict(), user_id=current_user.id)
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
        logger.info(f"Order created successfully. ID: {new_order.order_id}, User: {current_user.username}")
        return new_order
    except Exception as e:
        logger.exception(f"Error creating order: {e}")
        raise HTTPException(status_code=500, detail="Error creating order.")

# ==========================================================
# Get All Orders (Requires Authentication)
# ==========================================================
@router.get("/", response_model=List[schemas.Order])
def get_all_orders(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
) -> List[schemas.Order]:
    """Retrieve all orders belonging to the current user."""
    try:
        orders = db.query(models.Order).filter(models.Order.user_id == current_user.id).all()
        if not orders:
            logger.warning(f"No orders found for user: {current_user.username}")
        return orders
    except Exception as e:
        logger.exception(f"Error retrieving orders for {current_user.username}: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving orders.")

# ==========================================================
# Add Item to TEMP Order
# ==========================================================
@router.post("/add_item/", status_code=status.HTTP_200_OK)
def add_item_to_order(
    product_id: int,
    quantity: int = 1,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Add an item to the user's TEMP order (cart)."""
    try:
        product = db.query(models.Product).filter(models.Product.product_id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found.")

        if product.stock_amount < quantity:
            raise HTTPException(status_code=400, detail="Insufficient stock available.")

        order = db.query(models.Order).filter(
            models.Order.user_id == current_user.id,
            models.Order.status == models.OrderStatus.TEMP
        ).first()

        if not order:
            order = models.Order(
                user_id=current_user.id,
                status=models.OrderStatus.TEMP,
                order_date=datetime.utcnow(),
                total_price=0.0
            )
            db.add(order)
            db.commit()
            db.refresh(order)

        product.stock_amount -= quantity
        order_item = models.OrderItem(order_id=order.order_id, product_id=product_id, quantity=quantity)
        db.add(order_item)
        order.total_price += product.price * quantity
        db.commit()

        logger.info(f"Added {quantity} x {product.name} to order {order.order_id} for {current_user.username}")
        return {"message": f"Added {quantity} x {product.name} to order {order.order_id}."}

    except Exception as e:
        logger.exception(f"Error adding product {product_id} to order: {e}")
        raise HTTPException(status_code=500, detail="Error adding item to order.")

# ==========================================================
# Close TEMP Order
# ==========================================================
@router.put("/close/{order_id}", status_code=status.HTTP_200_OK)
def close_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Close the user's TEMP order (checkout)."""
    try:
        order = db.query(models.Order).filter(
            models.Order.order_id == order_id,
            models.Order.user_id == current_user.id
        ).first()

        if not order:
            raise HTTPException(status_code=404, detail="Order not found.")

        if order.status == models.OrderStatus.CLOSE:
            return {"message": "Order already closed."}

        order.status = models.OrderStatus.CLOSE
        db.commit()

        logger.info(f"Order {order_id} closed successfully for user {current_user.username}")
        return {"message": f"Order {order_id} has been closed successfully."}

    except Exception as e:
        logger.exception(f"Error closing order {order_id}: {e}")
        raise HTTPException(status_code=500, detail="Error closing order.")
