from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend import models, schemas, database

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Payment)
def create_payment(payment: schemas.PaymentCreate, db: Session = Depends(get_db)):
    new_payment = models.Payment(**payment.dict())
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment

@router.get("/", response_model=list[schemas.Payment])
def get_all_payments(db: Session = Depends(get_db)):
    return db.query(models.Payment).all()

@router.get("/{payment_id}", response_model=schemas.Payment)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = db.query(models.Payment).filter(models.Payment.payment_id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="תשלום לא נמצא")
    return payment

@router.put("/{payment_id}", response_model=schemas.Payment)
def update_payment(payment_id: int, updated_payment: schemas.PaymentCreate, db: Session = Depends(get_db)):
    payment = db.query(models.Payment).filter(models.Payment.payment_id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="תשלום לא נמצא")
    for key, value in updated_payment.dict().items():
        setattr(payment, key, value)
    db.commit()
    db.refresh(payment)
    return payment

@router.delete("/{payment_id}")
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = db.query(models.Payment).filter(models.Payment.payment_id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="תשלום לא נמצא")
    db.delete(payment)
    db.commit()
    return {"message": "תשלום נמחק בהצלחה"}