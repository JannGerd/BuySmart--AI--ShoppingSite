from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator


class ProductCreate(BaseModel):
    name: str
    price: float = Field(..., gt=0, description="Price must be greater than zero")
    stock_amount: int = Field(..., ge=0, description="Stock must be zero or more")

class ProductOut(ProductCreate):
    product_id: int

    class Config:
        from_attributes = True


class CustomerBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    address: str
    username: str
    password: str

    @field_validator("password")
    @classmethod
    def validate_password_length(cls, v):
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters long")
        return v

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    customer_id: int

    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    customer_id: int
    order_date: datetime
    status: str

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    order_id: int

    class Config:
        from_attributes = True


class PaymentCreate(BaseModel):
    order_id: int
    amount: float
    payment_method: str
    paid_at: datetime

class Payment(PaymentCreate):
    payment_id: int

    class Config:
        from_attributes = True


class OrderItemBase(BaseModel):
    order_id: int
    product_id: int
    quantity: int = Field(..., gt=0, description="Quantity must be greater than zero")

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    order_item_id: int

    class Config:
        from_attributes = True


class UserWishlistBase(BaseModel):
    customer_id: int
    product_id: int

class UserWishlistCreate(UserWishlistBase):
    pass

class UserWishlist(UserWishlistBase):
    wishlist_id: int
    added_at: date

    class Config:
        from_attributes = True


class UserRegister(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    username: str
    password: str
    city: Optional[str] = None
    country: Optional[str] = None
    phone: Optional[str] = None

    @field_validator("password")
    @classmethod
    def validate_password_length(cls, v):
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters long")
        return v

class UserLogin(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    username: str

    class Config:
        from_attributes = True


class CustomerOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr

    class Config:
        from_attributes = True
