from pydantic import BaseModel
from datetime import datetime, date


class ProductCreate(BaseModel):
    name: str
    price: float
    stock_amount: int

class ProductOut(ProductCreate):
    product_id: int

    class Config:
        from_attributes = True


class CustomerBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    address: str
    username: str
    password: str

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


class UserWishlistCreate(BaseModel):
    customer_id: int
    product_id: int

class UserWishlist(UserWishlistCreate):
    wishlist_id: int

    class Config:
        from_attributes = True


class OrderItemBase(BaseModel):
    order_id: int
    product_id: int
    quantity: int

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