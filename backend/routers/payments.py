from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend import models, schemas, database
from backend.security import get_current_user
from typing import List
import logging

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
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
# Create Payment (Requires Authentication)
# ==================================================
@router.post("/", response_model=schemas.Payment, status_code=status.HTTP_201_CREATED)
def create_payment(
        payment: schemas.PaymentCreate,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user)
) -> schemas.Payment:
    """
    Create a new payment (requires authentication).
    """
    try:
        new_payment = models.Payment(**payment.dict())
        db.add(new_payment)
        db.commit()
        db.refresh(new_payment)
        logger.info(f"Payment created successfully. ID: {new_payment.payment_id}")
        return new_payment
    except Exception as e:
        logger.exception(f"Error creating payment: {e}")
        raise HTTPException(status_code=500, detail="Error creating payment.")


# ==================================================
# Retrieve All Payments (Requires Authentication)
# ==================================================
@router.get("/", response_model=List[schemas.Payment])
def get_all_payments(
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user)
) -> List[schemas.Payment]:
    """
    Retrieve all payments (for authenticated users).
    """
    try:
        payments = db.query(models.Payment).all()
        if not payments:
            logger.warning("No payments found in the database.")
        logger.info(f"{len(payments)} payments retrieved successfully.")
        return payments
    except Exception as e:
        logger.exception(f"Error retrieving payments: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving payments.")


# ==================================================
# Retrieve Payment by ID (Requires Authentication)
# ==================================================
@router.get("/{payment_id}", response_model=schemas.Payment)
def get_payment(
        payment_id: int,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user)
) -> schemas.Payment:
    """
    Retrieve a specific payment by its ID.
    """
    try:
        payment = db.query(models.Payment).filter(models.Payment.payment_id == payment_id).first()
        if not payment:
            logger.error(f"Payment not found. ID: {payment_id}")
            raise HTTPException(status_code=404, detail="Payment not found.")
        logger.info(f"Payment retrieved successfully. ID: {payment_id}")
        return payment
    except Exception as e:
        logger.exception(f"Error retrieving payment {payment_id}: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving payment.")


# ==================================================
# Update Payment (Requires Authentication)
# ==================================================
@router.put("/{payment_id}", response_model=schemas.Payment)
def update_payment(
        payment_id: int,
        updated_payment: schemas.PaymentCreate,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user)
) -> schemas.Payment:
    """
    Update an existing payment by its ID.
    """
    try:
        payment = db.query(models.Payment).filter(models.Payment.payment_id == payment_id).first()
        if not payment:
            logger.error(f"Payment not found for update. ID: {payment_id}")
            raise HTTPException(status_code=404, detail="Payment not found.")

        for key, value in updated_payment.dict().items():
            setattr(payment, key, value)

        db.commit()
        db.refresh(payment)
        logger.info(f"Payment updated successfully. ID: {payment_id}")
        return payment
    except Exception as e:
        logger.exception(f"Error updating payment {payment_id}: {e}")
        raise HTTPException(status_code=500, detail="Error updating payment.")


# ==================================================
# Delete Payment (Requires Authentication)
# ==================================================
@router.delete("/{payment_id}", status_code=status.HTTP_200_OK)
def delete_payment(
        payment_id: int,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user)
) -> dict:
    """
    Delete a payment by its ID.
    """
    try:
        payment = db.query(models.Payment).filter(models.Payment.payment_id == payment_id).first()
        if not payment:
            logger.error(f"Payment not found for deletion. ID: {payment_id}")
            raise HTTPException(status_code=404, detail="Payment not found.")

        db.delete(payment)
        db.commit()
        logger.info(f"Payment deleted successfully. ID: {payment_id}")
        return {"message": "Payment deleted successfully."}
    except Exception as e:
        logger.exception(f"Error deleting payment {payment_id}: {e}")
        raise HTTPException(status_code=500, detail="Error deleting payment.")
