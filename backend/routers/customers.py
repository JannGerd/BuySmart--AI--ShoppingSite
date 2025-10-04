from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import Customer, Order, Payment, User
from backend.schemas import CustomerCreate, CustomerOut
from backend.security import get_current_user
from typing import List
import logging

router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)

logger = logging.getLogger(__name__)

# ==========================================
# Create Customer (Registration) – Open
# ==========================================
@router.post("/", response_model=CustomerOut, status_code=status.HTTP_201_CREATED)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)) -> CustomerOut:
    """
    Create a new customer (registration endpoint).
    """
    try:
        existing_customer = db.query(Customer).filter(Customer.email == customer.email).first()
        if existing_customer:
            logger.warning(f"Attempted to create customer with existing email: {customer.email}")
            raise HTTPException(status_code=400, detail="Email already registered")

        new_customer = Customer(**customer.dict())
        db.add(new_customer)
        db.commit()
        db.refresh(new_customer)
        logger.info(f"Created new customer: {new_customer.id}")
        return new_customer
    except Exception as e:
        logger.exception
